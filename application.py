import os

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha256
from datetime import datetime

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
    """ Login existing user """

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
                wrong_pw = "Incorrect Password for this Username"
                return render_template("login.html", message=wrong_pw)
        else:
            user_not_found = "Username Not Found"
            return render_template("login.html", message=user_not_found)

@app.route("/register", methods=["POST", "GET"])
def register():
    """ Register new user """

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
                success_message = "Registration Successful, Login Below"
                return render_template("login.html", message=success_message)
            # If username already in DB, cannot register
            else:
                error_message = "Username Already Exists, Cannot Register with this Username"
                return render_template("register.html", message=error_message)
        else:
            pw_mismatch = "Passwords Do Not Match"
            return render_template("register.html", message=pw_mismatch)

@app.route("/logout", methods=["POST"])
def logout():
    """ Logout user"""
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
    """ Search for a location given a zipcode or city """

    if request.method == "GET":
        try:
            return render_template("search.html", user=session["username"])
        except Exception as e:
            return redirect(url_for("login"))
    elif request.method == "POST":
        search_string = request.form.get("search")

        if search_string:
            try:
                search_string = search_string.upper()
                search_string = f"%{search_string}%"
                locations = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode LIKE :search_string OR city LIKE :search_string", {"search_string": search_string}).fetchall()
            except Exception as e:
                search_string = f"%{search_string}%"
                locations = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode LIKE :search_string OR city LIKE :search_string", {"search_string": search_string}).fetchall()
            try:
                matches = len(locations)
                if matches == 0:
                    no_results_message = "There were No Results Matching Your Query"
                    return render_template("search.html", message=no_results_message, user=session["username"])
                else:
                    return render_template("results.html", user=session["username"], locations=locations)
            except Exception as e:
                return redirect(url_for("login"))
        else:
            empty_search_field = "Nothing Entered, Nothing to Search"
            try:
                return render_template("search.html", message=empty_search_field, user=session["username"])
            except Exception as e:
                return redirect(url_for("login"))

@app.route("/results/<string:city>/<zipcode>/<lat>/<longg>/<string:check_in>", methods=["POST", "GET"])
def location(city, zipcode, lat, longg, check_in):
    """ Unique weather report for a location, also displays comments and check_in count """

    KEY = "8565f94778670d37d36772bcc5b2a904"
    get_request = f"https://api.darksky.net/forecast/{KEY}/{lat},{longg}"
    weather = requests.get(get_request).json()
    weather_now = weather["currently"]
    humidity = weather_now["humidity"] * 100
    humidity = f"{humidity}%"
    human_time = datetime.fromtimestamp(int(weather_now["time"])).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Get unique location info from DB and send to location page
    unique_location = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode = :zipcode", {"zipcode":zipcode}).fetchone()
    location_id = db.execute("SELECT id FROM locations WHERE zipcode = :zipcode", {"zipcode":zipcode}).fetchone()[0]

    # User submitting comment and checking into location
    comment = request.form.get("comment")
    if (check_in == "YES") and (comment != ""):
        user_comments = db.execute("SELECT user_id, zipcode FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.zipcode = :zipcode AND comments.user_id = :user_id", {"zipcode":zipcode, "user_id": session["user_id"]}).rowcount
        if user_comments == 0:
            db.execute("INSERT INTO comments (comment, user_id, location_id) VALUES (:comment, :user_id, :location_id)", {"comment": comment, "user_id": session["user_id"], "location_id": location_id})
            db.commit()
            check_in_count = db.execute("SELECT zipcode FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.zipcode = :zipcode", {"zipcode":zipcode}).rowcount
            comments_at_location = db.execute("SELECT username, comment FROM comments JOIN users ON users.id = comments.user_id WHERE location_id = :location_id", {"location_id":location_id}).fetchall()
            try:
                return render_template("location.html", city=city, lat=lat, longg=longg, zipcode=zipcode, zip_info=unique_location, check_in_count=check_in_count, weather_now=weather_now, humidity=humidity, human_time=human_time, user=session["username"], comments_at_location=comments_at_location)
            except Exception as e:
                return redirect(url_for("login"))
        else:
            check_in_count = db.execute("SELECT zipcode FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.zipcode = :zipcode", {"zipcode":zipcode}).rowcount
            comments_at_location = db.execute("SELECT username, comment FROM comments JOIN users ON users.id = comments.user_id WHERE location_id = :location_id", {"location_id":location_id}).fetchall()
            comment_error = "You Cannot Check In Again to the Same Location"
            try:
                return render_template("location.html", city=city, lat=lat, longg=longg, zipcode=zipcode, zip_info=unique_location, check_in_count=check_in_count, weather_now=weather_now, humidity=humidity, human_time=human_time, user=session["username"], comments_at_location=comments_at_location, message=comment_error)
            except Exception as e:
                return redirect(url_for("login"))

    comments_at_location = db.execute("SELECT username, comment FROM comments JOIN users ON users.id = comments.user_id WHERE location_id = :location_id", {"location_id":location_id}).fetchall()
    check_in_count = db.execute("SELECT zipcode FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.zipcode = :zipcode", {"zipcode":zipcode}).rowcount
    try:
        return render_template("location.html", city=city, lat=lat, longg=longg, zipcode=zipcode, zip_info=unique_location, check_in_count=check_in_count, weather_now=weather_now, human_time=human_time, humidity=humidity, user=session["username"], comments_at_location=comments_at_location)
    except Exception as e:
        return redirect(url_for("login"))

@app.route("/api/<string:zipcode>", methods=["GET"])
def weather_api(zipcode):
    """ GET Request API that returns location and check_in data from DB """

    location_data = db.execute("SELECT zipcode, city, state, lat, long, population FROM locations WHERE zipcode = :zipcode", {"zipcode": zipcode})
    if location_data.rowcount == 1:
        location_data = location_data.fetchone()
        check_in_count = db.execute("SELECT * FROM comments JOIN locations ON locations.id = comments.location_id WHERE locations.zipcode = :zipcode", {"zipcode":zipcode}).rowcount

        results = {
            "place_name": location_data.city,
            "state": location_data.state,
            "latitude": float(location_data.lat),
            "longitude": float(location_data[4]),
            "zip": location_data.zipcode,
            "population": location_data.population,
            "check_ins": check_in_count
        }

        results = jsonify(results)

        return results
    else:
        return jsonify(error=404), 404
