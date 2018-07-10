import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha256

import requests, json


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    """ Home Page """
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    """ Login """

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        pw_hash = sha256(password.encode()).hexdigest()

        # Check if username exists in DB
        if db.execute("SELECT username FROM users WHERE username = :username ", {"username":username}).rowcount == 1:
            true_pw_hash = db.execute("SELECT pw_hash FROM users WHERE username = :username ", {"username":username}).fetchall()[0][0]
            if(pw_hash == true_pw_hash):
                # If username and pw correct, login and redirect to search page
                session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username ", {"username":username}).fetchall()[0][0]
                session["username"] = username
                return redirect(url_for('search', action='search'))
            else:
                wrong_pw = "incorrect password for this username"
                return render_template("login.html", message=wrong_pw)
        else:
            user_not_found = "username not found"
            return render_template("login.html", message=user_not_found)

@app.route("/register", methods=["POST", "GET"])
def register():
    """ Register """

    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        verify_password = request.form.get("verify_password")

        if password == verify_password:
            pw_hash = sha256(password.encode()).hexdigest()

            # Make sure username is not already in DB
            if db.execute("SELECT username FROM users WHERE username = :username ", {"username":username}).rowcount == 0:
                db.execute("INSERT INTO users (username, pw_hash) VALUES (:username, :pw_hash)", {"username": username, "pw_hash": pw_hash})
                db.commit()
                success_message = "registration successful, login below"
                return render_template("login.html", message=success_message)
            # If username already in DB, cannot register
            else:
                error_message = "username already exists, cannot register with this username"
                return render_template("register.html", message=error_message)
        else:
            pw_mismatch = "passwords do not match"
            return render_template("register.html", message=pw_mismatch)

@app.route("/logout", methods=["POST"])
def logout():
    try:
        if session["user_id"] and session["username"]:
            del session["user_id"]
            del session["username"]
            return render_template("home.html")
    except Exception as e:
        print(f"User already logged out. {e}")
        return render_template("home.html")

@app.route("/<string:action>", methods=["POST", "GET"])
def search(action):

    if request.method == "GET":
        try:
            return render_template("search.html", user=session["username"])
        except Exception as e:
            return redirect(url_for("login"))
    elif request.method == "POST":
        search_string = request.form.get("search")

        if search_string:
            if search_string.isalpha():
                search_string = search_string.upper()
            search_string = f"{search_string}%"
            locations = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode LIKE :search_string OR city LIKE :search_string", {"search_string": search_string}).fetchall()
            return render_template("results.html", user=session["username"], locations=locations)
        else:
            empty_search_field = "Nothing entered, nothing to search"
            return render_template("search.html", message=empty_search_field, user=session["user_id"], username=session["username"])

@app.route("/results/<string:city>/<zipcode>/<lat>/<longg>")
def location(city, zipcode, lat, longg):

    KEY = "8565f94778670d37d36772bcc5b2a904"
    get_request = f"https://api.darksky.net/forecast/{KEY}/{lat},{longg}"
    weather = requests.get(get_request).json()
    weather_now = weather["currently"]

    # Get unique location info from DB and send to location page
    unique_location = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode = :zipcode", {"zipcode":zipcode}).fetchone()
    check_in = db.execute("SELECT zipcode FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.z")

    return render_template("location.html", city=city, lat=lat, longg=longg, zipcode=zipcode, zip_info=unique_location, weather_now=weather_now, user=session["username"])
