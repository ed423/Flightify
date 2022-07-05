from venv import create
from flask import Flask, url_for, redirect, render_template, session, request, render_template
from flask_session import Session
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Load dotenv
load_dotenv()

# Load client ID, client secret and redirect URI from dotenv file
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')

cache = '.spotipyoauthcache'
scope = 'playlist-modify-public user-top-read'
token_key = 'token_key'

# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64).hex()
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'yummy cookie'
Session(app)

# Endpoints
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login(): 
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/success")
def success():
    sp_oauth = create_spotify_oauth()
    session.clear()
    print('getting code...')
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    print('saving token info to session...')
    session[token_key] = token_info
    return redirect(url_for('flights', external=True))

@app.route("/flights")
def flights():
    sp_oauth = create_spotify_oauth()
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    results = sp.current_user_playlists(limit=20)
    for i, item in enumerate(results['items']):
        print("%d %s" % (i, item['name']))
    return "Got playlists"

def create_spotify_oauth():
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=url_for('success', _external=True), scope=scope)


















