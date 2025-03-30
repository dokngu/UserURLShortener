import random
import string

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
urls = {} # TODO: replace this with actual SQL DB

def generate_short_url(length=8):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

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
