from venv import create
from flask import Flask, url_for, redirect, render_template, session, request, render_template
from flask_session import Session
from dotenv import load_dotenv
import spotipy
import json
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
    # return redirect(url_for('playlist', external=True))
    return render_template('generate_playlist.html')

# @app.route("/playlist")
# def playlist():
#     sp_oauth = create_spotify_oauth()
#     sp = spotipy.Spotify(auth_manager=sp_oauth)

#     available_genres = sp.recommendation_genre_seeds()
#     genre_list = available_genres['genres']
#     # print(genre_list)

#     recommendation = get_recommendation('pop')
#     id = recommendation['tracks'][0]['id']
#     name = recommendation['tracks'][0]['name']
#     time = recommendation['tracks'][0]['duration_ms']
#     print(recommendation['tracks'][0]['id'], '\n', recommendation['tracks'][0]['name'], '\n', recommendation['tracks'][0]['duration_ms'])
#     return "got recommended tracks"
    
# Initiates playlist generation
@app.route("/generate", methods=['GET', 'POST'])
def generate():
    sp_oauth = create_spotify_oauth()
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    name = request.form['name']
    genre = request.form['genre']
    length = request.form['length']
    length_in_ms = int(length) * 60 * 60 * 1000
    # print(length_in_ms)

    playlist = create_playlist(name)
    playlist_id = playlist["id"]
    time_so_far = 0

    while time_so_far < length_in_ms:
        recommendations = sp.recommendations(seed_genres=[genre], limit=1)
        recommended_track_id = recommendations['tracks'][0]['id']
        track_id_as_array = [recommended_track_id]
        time_so_far += recommendations['tracks'][0]['duration_ms']
        sp.playlist_add_items(playlist_id=playlist_id, items=track_id_as_array)
        print(time_so_far)

    return "generated playlist"

@app.route("/about")
def about():
    return render_template('about.html')

# Helper functions

def create_spotify_oauth():
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=url_for('success', _external=True), scope=scope)

def create_playlist(name):
    sp_oauth = create_spotify_oauth()
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    uid = sp.me()['id']
    playlist = sp.user_playlist_create(user=uid, name=name)
    return playlist

def get_recommendation(genre):
    sp_oauth = create_spotify_oauth()
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    recommendations = sp.recommendations(seed_genres=[genre], limit=1)
    return recommendations['tracks'][0]['duration_ms']



















