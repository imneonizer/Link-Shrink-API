import flask
from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from shared.factories import db
from shared.config import config
from shared.utils import build_http_url
from models.urls import Urls
import requests
import json
import uuid
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/", methods=["post"])
def index():
    data = json.loads(request.data)
    # print(data)
    url, todo, key, verify = data.get("url", None), data.get("todo", None), data.get("key", None), data.get("verify", None)
    
    if todo == "short":
        query = Urls.query.filter(Urls.long_url == url).first()
        if query:
            # if Url already exists in the database then return it's short url
            # print({"url": query.short_url}, 200)
            return make_response({"url": query.short_url}, 200)
        
        iterations = 0
        while True:
            # if Url doesn't exists in database, but randomly generated short url is already present
            # then create another random short url until we get a unique random Url.

            try:
                # validate whether the long_url exists
                if verify:
                    requests.get(build_http_url(url))
            except requests.exceptions.InvalidURL:
                # return error message if invalid url passed
                return make_response({"message": f"InvalidUrl: {url}"}, 400)
            except requests.exceptions.ConnectionError:
                # return error message if url doesn't exists
                return make_response({"message": f"url: '{url}', doesn't exists or not responding."}, 400)
            
            # generate a random short url key
            short_url_key = str(uuid.uuid1())[:8]
            
            if key:
                # if custom short url key is passed then mutate it with random capitalization
                if iterations <= 100:
                    # if all the random mutations exceeded 100 limit
                    # and no unique mutation found, then don't use the key.
                    short_url_key = ''.join(random.choice((str.upper, str.lower))(c) for c in key)
            
            short_url = config['DOMAIN']+"/"+short_url_key
            query = Urls.query.filter(Urls.short_url == short_url).first()

            if not query:
                # if the generated key is unique and is not already in the database
                # then add it to the database and return response
                db.session.add(Urls(short_url=short_url, long_url=url))
                db.session.commit()
                # print({"url": short_url}, 200)
                return make_response({"url": short_url}, 200)
            
            # keep a count of how many attempts
            # required to generate the unique key
            iterations += 1

    elif todo == "long":
        # query the database for the short url
        query = Urls.query.filter(Urls.short_url == url).first()
        if query:
            # if short url exists in the database
            # then return its long url
            # print({"url": query.long_url}, 200)
            return make_response({"url": query.long_url}, 200)
        else:
            # if short url doesn't exists in the database then return 404
            return make_response({"message": "url not found"}, 404)

    else:
        # handle other errors
        return make_response({"message": f"unknown task: {todo}"}, 400)


@app.route("/<short_url_key>", methods=["get"])
def redirect(short_url_key):
    query = Urls.query.filter(Urls.short_url.endswith(short_url_key)).first()
    if query:
        # if url exists in the database then
        # redirect to long url
        return flask.redirect(build_http_url(query.long_url))
    
    # redirect to home page
    return  flask.redirect("/404")


@app.route("/404", methods=["get"])
def _404():
    # return custom 404 page  with 404 status code
    return make_response(render_template("404.html"), 404)


if __name__ == "__main__":
    app.run(debug=config['DEBUG'], host=config['HOST'], port=config['PORT'])