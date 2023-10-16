from flask import Flask, jsonify, request, redirect
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()
app = Flask(__name__)


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = "https://localhost:3000/auth"
session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)
session.scope = ["profile:read_all,activity:read"]

@app.route('/time')
def get_current_time():
    return {'time': 'hello'}

# https://stackoverflow.com/questions/21498694/flask-get-current-route


def authorize_url():
    auth_base_url = "https://www.strava.com/oauth/authorize"
    auth_link = session.authorization_url(auth_base_url)
    logger.debug(auth_link)
    return auth_link[0]


@app.route("/")
def home():
    logger.debug(request.path)
    return {'link': authorize_url()}


@app.route("/client")
def client():
    logger.debug(request.url)
    return "Welcome to cliet"


@app.route("/login")
def authorize():
    """Redirect user to the Strava Authorization page"""
    return redirect(authorize_url())


@app.route("/auth")
def authorization_successful():
    token_url = "https://www.strava.com/api/v3/oauth/token"
    session.fetch_token(
    token_url=token_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=request.url,
    include_client_id=True)
    logger.debug(session.access_token)

    response = session.get("https://www.strava.com/api/v3/athlete")
    return response.text


@app.route("/athlete")
def athlete_data():
    response = session.get("https://www.strava.com/api/v3/athlete")
    return response.text

@app.route("/activities")
def activity_data():
    activities = session.get("https://www.strava.com/api/v3/athlete/activities")
    return activities.text



if __name__ == '__main__':
   
    app.run(host="localhost", port=3000, debug=True, ssl_context='adhoc')
