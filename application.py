import os

from flask import Flask, session, render_template
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
    KEY = "8565f94778670d37d36772bcc5b2a904"
    get_request = f"https://api.darksky.net/forecast/{KEY}/42.37,-71.11"
    weather = requests.get(get_request).json()
    summary = weather["currently"]["summary"]
    #print(json.dumps(weather["currently"], indent = 2))
    return render_template("home.html", summary=summary)
