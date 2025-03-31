import bcrypt
import random
import string
import pymysql.cursors
import json
import settings
import cgitb
import cgi
import sys
from flask import Flask, render_template, redirect, request, jsonify, abort, request, make_response
#from flask_restful import Resource, Api
cgitb.enable()

from db_util import db_access # db code in db_util.py

app = Flask(__name__, static_url_path='/static')
# api = Api(app)
urls = {} # TODO: replace this with actual SQL DB

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
    
def check_creds(username, pw):


    
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
@app.route("/users/new", methods=["GET","POST"])
def new_user_form():
    if request.method == "POST":
        username = request.form['username'];
        password = hash_pw(request.form['password']);
        email = request.form['email'];
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
    return render_template("newuser.html")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
    # TODO: Refactor to use with stored procedures & SQL DB
        while short_url in urls: 
            short_url = generate_short_url()

        urls[short_url] = long_url
        return f"Shortened URL: {request.url_root}urls/{short_url}"
    return render_template("index.html")

@app.route("/urls/<short_url>")
def redirect_url(short_url):
    # TODO: Refactor to use with stored procedures & SQL DB
    long_url = urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
