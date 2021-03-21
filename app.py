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

# name_author="Bob_Marley"


@app.route("/")
@app.route("/home")
def welcome():
    routes = {"/api/v1.0/quotes": " - Quotes",
              "/api/v1.0/authors": " - List of Authors",
              "/api/v1.0/authors/Bob%20Marley": " - Search for an Author, for example: Bob Marley.",
              "/api/v1.0/tags": " - List of tags associated to quotes",
              "/api/v1.0/tags/love": " - Search for a tags associated to quotes, for example: love",
              "/api/v1.0/toptentags": " - List of top 10 tags for all quotes scraped, for examaple: /api/v1.0/love"
              }
    return render_template('index.html', message="Available Routes", quote_link=routes)


@app.route("/api/v1.0/quotes")
def quotes():
    quotes_data = list(mdb.quotes_everything_collection.find())

    clean_quotes_data = []
    for q in quotes_data:
        q.pop('_id')
        q.pop('author_description')
        q.pop('author_born')
        clean_quotes_data.append(q)

    return jsonify({"Quotes": clean_quotes_data, "Number of Quotes": len(clean_quotes_data)})


@app.route("/api/v1.0/authors")
def authors():
    quotes_data = list(mdb.quotes_everything_collection.find())
    unique_authors = []
    author_list_details = []
    for q in quotes_data:
        num_quotes = 0
        if q['author_name'] not in unique_authors:
            unique_authors.append(q['author_name'])
        for author in quotes_data:
            if author['author_name'] == unique_authors[-1]:
                num_quotes += 1
        author_details = {"name": q["author_name"],
                          "description": q['author_description'],
                          "born": q['author_born'],
                          'count': num_quotes,
                          'quotes': [{"text": q["quote_text"], "tags":q["tags"]}]
                          }
        author_list_details.append(author_details)

    return jsonify({"Author Total": len(unique_authors), "details": author_list_details})


@ app.route("/api/v1.0/authors/<author_name>")
def author_name(author_name):
    # author_name=author_name.str.replace("_"," ",1)
    quotes_data = list(mdb.quotes_everything_collection.find())
    # author_quotes=list(mdb.quotes_everything_collection.find_one({"author_name",author_name}))
    author_info = mdb.author_information_collection.find_one(
        {'name': 'Bob Marley'})
    author_info.pop('_id')
    print(author_name)
    quotes_and_tags_list = []
    num_quotes = 0
    for q in quotes_data:
        print(q)
        if q["author_name"] == author_name:
            num_quotes += 1
            quotes_and_tags_dict = {"text": q["quote_text"], "tags": q["tags"]}
            quotes_and_tags_list.append(quotes_and_tags_dict)
    # for x in author_list_details:
    #     x['number_of_quotes'] = num_quotes
    # Docstring
    # """Return a JSON list of author names for quotes"""
    author_info['number_of_quotes'] = num_quotes
    author_info['quotes'] = quotes_and_tags_list
    return jsonify(author_info)


@ app.route("/api/v1.0/tags")
def tags():
    # """Returns a list of tags assigned to quotes"""
    tag_list = []

    for tag in mdb.tags_collection.find({}, {"_id": 0, "tag": 1}):
        tag_list.append(tag['tag'])

    q_and_t = list(mdb.tag_relation_collection.find(
        {}, {"_id": 0, "tag": 1, "quote_text": 1}))

    details = []
    for tag in tag_list:
        tcount = 0
        quotes = []
        for qt in q_and_t:
            for t in qt['tag']:
                if t == tag:
                    tcount += 1
                    quotes.append(
                        {"text": qt["quote_text"], "tags": qt['tag']})
        details.append(
            {"name": tag, "number_of_quotes": tcount, "quotes": quotes})

    final_tag_dict = {"count": len(tag_list), "details": details}
    return jsonify(final_tag_dict)


@ app.route("/api/v1.0/tags/<tag_name>")
def tag_search(tag_name):
    print(tag_name)
    tag_details = list(mdb.tag_relation_collection.find({"tag": tag_name}))
    details = []
    quotes = []
    tcount = 0
    for tag in tag_details:
        tcount += 1
        quotes.append({"quote": tag["quote_text"], "tags": tag['tag']})
    details.append({"tag": tag_name, "count": tcount, "quotes": quotes})
    return jsonify(details[0])


@ app.route("/api/v1.0/toptentags")
def top_ten():
    # Docstring
    # """Return a list of the top ten tags associated with the quotes."""
    tag_list = []
    for tag in mdb.tags_collection.find({}, {"_id": 0, "tag": 1}):
        tag_list.append(tag['tag'])

    q_and_t = list(mdb.tag_relation_collection.find(
        {}, {"_id": 0, "tag": 1, "quote_text": 1}))

    details = []
    for tag in tag_list:
        tcount = 0
        quotes = []
        for qt in q_and_t:
            for t in qt['tag']:
                if t == tag:
                    tcount += 1
                    quotes.append(
                        {"text": qt["quote_text"], "tags": qt['tag']})
        details.append({"tag": tag, "quote_count": tcount})

    detailsf = {"details": details}
    len_tags = len(detailsf['details'])

    quote_count_number = []
    top_ten = []
    for i in detailsf['details']:
        quote_count_number.append(i['quote_count'])

    sorted_count = sorted(quote_count_number, reverse=True)[0:9]

    for x in range(len_tags):
        if detailsf['details'][x]['quote_count'] in sorted_count:
            top_ten.append(detailsf['details'][x])

    return jsonify(top_ten)


if __name__ == '__main__':
    app.run(debug=True)
