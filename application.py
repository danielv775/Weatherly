import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

    KEY = "8565f94778670d37d36772bcc5b2a904"
    get_request = f"https://api.darksky.net/forecast/{KEY}/42.37,-71.11"
    weather = requests.get(get_request).json()
    summary = weather["currently"]["summary"]
    #print(json.dumps(weather["currently"], indent = 2))
    return render_template("home.html", summary=summary)

@app.route("/search", methods=["POST"])
def login_register():
    """ Login or Register """

    user_name = request.form.get("username")
    pass_word = request.form.get("password")

    if request.form["submit"] == "Login":

        # Check if username exists in DB. If it doesn't alert user that they must Register

        # If username exists and password correct
        return render_template("search.html", user_name=user_name)

        # If username exists but password wrong, alert user they must re-enter password

    elif request.form["submit"] == "Register":

        # Make sure username is not in DB. If username is in DB, alert user they must Login. Not Register.

        # If username not in DB, Allow user to register and take them to search page

        return render_template("search.html", user_name=user_name)
