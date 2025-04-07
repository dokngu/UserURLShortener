import bcrypt
import random
import string
import pymysql.cursors
import json
import settings
import cgitb
import cgi
import sys
from flask import Flask, render_template, redirect, request, jsonify, abort, request, make_response, url_for, session, flash
#from flask_cors import CORS
from flask_restful import Resource, Api
from urllib.parse import urlparse
cgitb.enable()

from db_util import db_access # db code in db_util.py

app = Flask(__name__, static_url_path='/static')
app.secret_key = settings.SECRET_KEY

# DISABLE/COMMENT OUT THIS LINE IN PRODUCTION
#CORS(app)


api = Api(app)
#####################
#
# Functions
#
def generate_short_url(length=8):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

def hash_pw(pw):
    salt = bcrypt.gensalt() # random salt
    hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8') # return encoded pw


    
###################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
    return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
    return make_response(jsonify( { "status": "Resource not found" } ), 404)

####################################################################################
#
# Static Endpoints for humans
#

#####################################################
#
# users routing: POST
#    
#@app.route("/users/new", methods=["GET","POST"])
@app.route("/users/new", methods=["POST"])
def create_user():
    if request.method == "POST":
        username = request.json['username'];
        password = hash_pw(request.json['password']);
        email = request.json['email'];
        if not username or not password or not email: 
            abort(400)
	
        sqlProc = 'createUser'
        sqlArgs = [username, password, email]
        try:
            row = db_access(sqlProc, sqlArgs)
        except Exception as e:
            print("caught an exception!!")
            abort(500, message = e) # server err
        uri = request.base_url+'/'+str(row[0]['LAST_INSERT_ID()'])
        return make_response(jsonify( { "uri": uri } ), 201)
    # return render_template("newuser.html")
    
#@app.route("/login", methods=["GET","POST"])
@app.route("/login", methods=["POST"])
def login():
    if 'username' in session:
        print("Authenticated, redirecting to main")
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.json['username'];
        password = request.json['password'].encode('utf-8');
        # get data from SQL
        sqlProc = 'verifyCreds'
        sqlArgs = [username]
        try:
            row = db_access(sqlProc, sqlArgs)
            dbpw = row[0]['pw_hash'].encode('utf-8')
            print(dbpw)
            if bcrypt.checkpw(password, dbpw):
                session['username'] = username
                # flash('Successfully logged in', 'success')
                # return redirect(url_for('index'))
                response = {'message': 'Logged in successfully'}
                responseCode = 200
                return make_response(jsonify(response),responseCode)
            else:
                # flash('Invalid credentials.', 'danger')
                # return redirect(url_for('login'))
                response = {'message': 'Bad credentials'}
                responseCode = 401
                return make_response(jsonify(response),responseCode)
        except Exception as e:
            print("caught an exception!!")
            abort(500, description=str(e)) # server err
            
    #if GET return this        
    #return render_template('login.html')

#@app.route("/", methods=["GET","POST"])
@app.route("/urls", methods=["POST"])
def create_short_url():

    if 'username' not in session:
        print("Not authenticated")
        response = {'message': 'Unauthenticated user'}
        responseCode = 401
        return make_response(jsonify(response),responseCode)
        
    if request.method == "POST":
        username = session['username']
        long_url = request.json['long_url']
        
        # links that do not start with 'http://' do not properly redirect. This fixes that.
        parse_url = urlparse(long_url)
        if not parse_url.scheme:
            long_url = "http://" + long_url # just add it in manually lol
        
        short_url = generate_short_url()
        
        # get data from SQL
        sqlProc = 'getUserID'
        sqlArgs = [username]
        userID = 0 # default dummy uid
        try:
            row1 = db_access(sqlProc, sqlArgs)
            userID = row1[0]['user_id']
            sqlProc = 'createShort'
            sqlArgs = [short_url, long_url, userID]
            print("short: " + short_url)
            print("long: " + long_url)
            row2 = db_access(sqlProc, sqlArgs)
        except Exception as e:
            print("caught an exception!!")
            print(str(e))
            abort(500, description=str(e)) # server err
        response = {'link' : f'{request.host_url}urls/{short_url}'}
        responseCode = 201
        return make_response(jsonify(response), responseCode)    
        
    # if GET return this
    #return render_template("index.html")

@app.route("/urls/<short_url>", methods=["GET"])
def redirect_url(short_url):
    print('short_url = ' + short_url)
    sqlProc = 'getLink'
    sqlArgs = [short_url]
    try:
        row = db_access(sqlProc, sqlArgs)
        long_url = row[0]['original_url']
        return redirect(long_url)
    except Exception as e:
        print("caught an exception!!")
        errMsg = str(e)
        print(errMsg)
        abort(404, description="Link not found") if (errMsg == "tuple index out of range") else abort(500, description=str(e)) # server err
        
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    # flash('Logging you out', 'info')
    response = {'message': 'Logged out successfully'}
    responseCode = 200
    return make_response(jsonify(response), responseCode)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context, debug=settings.APP_DEBUG)
    #app.run(debug=True, ssl_context=context)
