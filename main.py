import requests
import urllib.parse
import spotifyEnvironment
import spotipy
import json

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session


app = Flask(__name__)
app.secret_key = '123k48907864g256-2345kn-2345234v5o-234lk5hjl23'

CLIENT_ID = spotifyEnvironment.client_id
CLIENT_SECRET = spotifyEnvironment.client_secret
REDIRECT_URI = spotifyEnvironment.redirect_uri

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify/com/v1/'


@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public app-remote-control'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    # Build request body if code is sent back from spotify
    if 'code' in request.args:
        request_body = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=request_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']      
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    return redirect('/playlsits')

@app.route('/playlists')
def getPlaylists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() >= session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }

    response = request.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    
    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() >= session['expires_at']:
        req_body = {
            'grant_type' : 'refresh_token',
            'refresh_token' : session['refresh_token'],
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token = response.json()

        session['access_token'] = new_token['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token['expires_in']

        return redirect('/playlsits')

@app.route('/likedsongs')
def getLikedSongs(token):
    #get songs from Liked Songs
    songs = {}
    genres = {}
    i = 0
    
    if token:
        sp1 = spotipy.Spotify(auth=token)
        liked_songs = sp1.current_user_saved_tracks()
        size = liked_songs['total']
        print("Starting while loop\n")

        while i < size:

            sp = spotipy.Spotify(auth=token)
            # Results stores songs in clusters of 50
            results = sp.current_user_saved_tracks(offset=i, limit=50)
            songs[i] = results

            i += 50
        print("\nSongs finished being parsed\n")
    with open('songs.json', 'w') as fp:
        json.dump(songs, fp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)