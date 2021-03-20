import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import pword, database, username
from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
# import scrape_phone

#################################################
# Database Setup
#################################################
# <=== username is postgres and mypassword is next
postgres_database = f"postgresql://{username}:{pword}@localhost:5432/{database}"
engine = create_engine(postgres_database)
conn_sql = engine.connect()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# Create connection variable
conn_mongo = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn_mongo)
mdb = client.quotes_db


@app.route("/")
@app.route("/home")
def welcome():
    #"""List all available api routes."""
    # (

    #      f"Available Routes:<br/>"
    #      f"/api/v1.0/quotes"
    #      f" - Quotes<br/>"

    #      f"/api/v1.0/authors"
    #      f" - List of authors<br/>"

    #      f"/api/v1.0/authors/< author name >"
    #      f" - Search for an Author<br/> for examaple, author first name last name"

    #      f"/api/v1.0/tags"
    #      f" - List of tags associated to quotes<br/>"

    #      f"/api/v1.0/tags/<tag>"
    #      f" - Search for a tags associated to quotes<br/>"

    #      f"/api/v1.0/top10tags"
    #      f" - List of top 10 tags for all quotes scraped<br/> for examaple, /api/v1.0/love"
    # )
    routes = {"/api/v1.0/quotes": " - Quotes",
              "/api/v1.0/authors": " - List of Authors",
              "/api/v1.0/authors/< author name >": " - Search for an Author, for example: author first name, last name.",
              "/api/v1.0/tags": " - List of tags associated to quotes",
              "/api/v1.0/tags/<tag>": " - Search for a tags associated to quotes",
              "/api/v1.0/top10tags": " - List of top 10 tags for all quotes scraped, for examaple: /api/v1.0/love"
              }
    return render_template('index.html', message="Available Routes", quote_link=routes)


@app.route("/api/v1.0/quotes")
def quotes():
    quotes_data = list(mdb.quotes_everything_collection.find())

    clean_quotes_data = []
    for q in quotes_data:
        q.pop('_id')
        clean_quotes_data.append(q)

    return jsonify({"Quotes": clean_quotes_data, "Number of Quotes": len(clean_quotes_data)})


@app.route("/api/v1.0/authors")
def authors():

    #"""Return a list of authors of scrapped quotes"""
    return 0


@app.route("/api/v1.0/<author_name>")
def author_name(author_name):
    # Docstring
    #"""Return a JSON list of author names for quotes"""
    return 0


@app.route("/api/v1.0/tags")
def tags():
    #"""Returns a list of tags assigned to quotes"""
    return 0


@app.route("/api/v1.0/<tag>")
def tag_search(tag):
    # Docstring
    # search for tag
    return 0


@app.route("/api/v1.0/toptentags")
def top_ten():
    # Docstring
    #"""Return a list of the top ten tags associated with the quotes."""
    return 0


if __name__ == '__main__':
    app.run(debug=True)
