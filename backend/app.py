from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env' #explicitly get the path for the .env file
load_dotenv(dotenv_path=env_path)
import time
import requests
import urllib.parse
import spotipy
import json
import os, hashlib, re
from datetime import datetime, timedelta
from flask import Flask, Response, flash, redirect, request, jsonify, send_from_directory, session, Blueprint, render_template, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, update, delete


app = Flask(__name__.split('.')[0], static_folder='static', template_folder='templates')
app.secret_key = '123k48907864g256-2345kn-2345234v5o-234lk5hjl23'
app.config.from_object('config.Config')
sonos_db = SQLAlchemy(app)

CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
REDIRECT_URI = os.getenv("redirect_uri")

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

import models.tables as tables

with app.app_context():
    sonos_db.create_all()


def get_hashed_filename(filename):
    build_dir = os.path.abspath(os.path.join(app.root_path, '..', 'frontend', 'sonora_client', 'build', 'static'))
    pattern = re.compile(f"{re.escape(filename)}\\.[a-f0-9]+\\.{filename.split('.')[-1]}")
    print("Build Directory:", build_dir)

    files = os.listdir(build_dir)
    for file in files:
        if pattern.match(file):
            return file

    return filename

# Get the absolute path to the 'css' folder within the Flask app directory
css_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css')

# @app.before_request
# def require_login():
#     allow = ['first', 'login', 'callback']
#     print(session)
#     if request.endpoint not in allow and 'access_token' not in session:
#         return redirect('/login')

@app.route('/css/sonora_styles.css')
def serve_css(filename):
    return send_from_directory(css_folder, filename)


@app.route('/')
def first():
    return render_template('login.html', get_hashed_filename=get_hashed_filename)


@app.route('/login')
def login():
    print("\nLogin Beginning\n")
    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public app-remote-control'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print("\nLogin Finishing =========================\n")
    print("\nAuth Url: ", auth_url, "\n")
    return redirect(auth_url), print("Done fr")

@app.route('/callback')
def callback():
    print("\nCallback Begin\n")
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

        if 'error' in token_info:
            print("Token Retrieval Error:", token_info['error'])
            flash('User login failed. Please enter valid account credentials or check your internet connection', 'error')
            # Handle the error (e.g., redirect to login page)
            # return redirect('/login')
        else:
            print("\nToken Retrieval Response: ", token_info) 

            session['access_token'] = token_info['access_token']
            session['refresh_token'] = token_info['refresh_token']      
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
            flash("Logged in")
    print("\nCallback End\n")
    return home()

@app.route('/home')
def home():
    print("\nHome Begin\n")
    if 'access_token' not in session:
        return redirect('/login')
    print("Access Token: ", session['access_token'])
    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me', headers=headers)
    
    if response.status_code != 200:
        print(f"\nFailed to retrieve playlists. Status Code: {response.status_code}\n Status Message:\n{response.text}")
        return render_template('query-error.html', get_hashed_filename=get_hashed_filename, status_code=response.status_code,
                               text=response.text)
    # TODO: make page for when query errors occur while users are attempting to use the service
    
    profile_info = response.json()
    session['profile_info'] = profile_info
    profile = True
    # if (tables.User.query.get(profile_info.id) == None):
    #     db_profile = insert(tables.User).values(id=profile_info.id,
    #                                     username=profile_info.display_name,
    #                                     email=profile_info.email,
    #                                     uri=profile_info.uri,
    #                                     xcont=profile_info.explicit_content,
    #                                     external_url=profile_info.external_urls,
    #                                     followers=profile_info.followers[2],
    #                                     url=profile_info.href,
    #                                     profilePic=profile_info.images,
    #                                     subscription=profile_info.product,
    #                                     type=profile_info.type)
    #     try:
    #         # Execute the insertion
    #         result = sonos_db.session.execute(db_profile)
    #         sonos_db.session.commit()
    #         print("User inserted successfully!")
    #     except Exception as e:
    #         sonos_db.session.rollback()
    #         print(f"Error inserting user: {e}")

    data = getPlaylists()[1]
    print("Get Playlist Data: ", data)
    totalPlaylists = data
    print("Total Playlists: ", totalPlaylists)
    # likedCats = getLikedCategories()
    # catg = session.get('categorized')
    # uncatg = session.get('uncategorized')
    # return render_template('index.html', get_hashed_filename=get_hashed_filename, profile_info=profile_info, profile=profile, totalPlaylists=totalPlaylists,
    #                        categorized=catg, uncategorized=uncatg)
    print("\nHome End\n")
    return render_template('index.html', get_hashed_filename=get_hashed_filename, profile_info=profile_info, profile=profile, totalPlaylists=totalPlaylists)

@app.route('/my-playlists')
def getPlaylists():
    print("Get Playlist function started\n")
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    
    if response.status_code != 200:
        print(f"\nFailed to retrieve playlists. Status Code: {response.status_code}\n Status Message:\n{response.text}")
        return render_template('query-error.html', get_hashed_filename=get_hashed_filename, status_code=response.status_code,
                               text=response.text)
    # TODO: make page for when query errors occur while users are attempting to use the service

    playlists = response.json()['items']
    print("Playlists API Response (JSON):", playlists)
    totalPlaylists=response.json()['total']
    profile_info = session.get('profile_info')
    return render_template('my-playlists.html', get_hashed_filename=get_hashed_filename, playlists=playlists, totalPlaylists=totalPlaylists, profile_info=profile_info), totalPlaylists  

# Get images for each playlist
@app.route('/getPlaylistImage/<playlist_id>')
def getPlaylistImage(playlist_id):
    print("Get Playlist Image function started\n")
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }
    urlbuild = API_BASE_URL + f'playlists/{playlist_id}/images'
    print("GET url: ", urlbuild)
    response = requests.get(urlbuild, headers=headers)
    if response.status_code != 200:
        print(f"\nFailed to retrieve playlist image. Status Code: {response.status_code}\n Status Message:\n{response.text}")
        # return render_template('query-error.html', get_hashed_filename=get_hashed_filename, status_code=cover.status_code,
                            #    text=cover.text)
    # TODO: make page for when query errors occur while users are attempting to use the service
    cover = response.json()[0]['url']
    print("Cover Url: ", cover)
    
    return cover


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

        return redirect('/my-playlists')


@app.route('/likedsongs')
def getLikedSongs():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    sp = spotipy.Spotify(auth=session['access_token'])
    #get songs from Liked Songs
    songs = {}
    songInfo = []
    genres = {}
    i = 0
    songslist = []
    trackids = []

    liked_songs = sp.current_user_saved_tracks()
    size = liked_songs['total']
    # print("Number of liked songs: ", size)
    # print("Liked_songs")
    # print("Starting while loop\n")
    while i < size:
        # Results stores songs in clusters of 50
        results = sp.current_user_saved_tracks(offset=i, limit=50)
        songs[i/50] = results
        # print("\n\nSongs Index: ", i)
        batch = songs[i/50]['items']
        batchids = []
        for song in batch:
            # print("\nSong: ", song['track']['name'], " by ", song['track']['artists'][0]['name'])
            track = song['track']['name']
            artist = song['track']['artists'][0]['name']
            songInfo.append((track, artist))
            batchids.append(song['track']['id'])
            # sonos_track = insert(tables.Track).values(
            #     spotify_id=song['track']['id'],
            #     title=track
            # )
        # yield jsonify({'batch': batch})
        # print("Batchids: ", ",".join(batchids))
        trackids.append(",".join(batchids))
        i += 50
    print("\nSongs finished being parsed\n")
    songslist.append(songs)

    # with open('songs.json', 'w') as fp:
    #     json.dump(songs, fp)
    return  render_template('likedsongs.html',
                             get_hashed_filename=get_hashed_filename,
                             songs=songs, songInfo=songInfo,
                             trackids=trackids), songInfo
    
@app.route('/getTrackImage/<track_id>')
def getTrackImage(track_id):
    # print("Get Track Image function started\n")
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }
    
    urlbuild = API_BASE_URL + f'tracks/{track_id}'
    # print("GET url: ", urlbuild)
    response = requests.get(urlbuild, headers=headers)
    
    if response.status_code != 200:
        print(f"\nFailed to retrieve track image. Status Code: {response.status_code}\n Status Message:\n{response.text}")
        # return render_template('query-error.html', get_hashed_filename=get_hashed_filename, status_code=cover.status_code,
                            #    text=cover.text)
    # TODO: make page for when query errors occur while users are attempting to use the service
    # print("\nResponse for Track Cover: ", response.json())
    
    cover = response.json()['album']['images'][0]['url']
    # print("Cover Url: ", cover)
    
    # covers = {}
    # for track in response.json():
    #     print("\nTrack from Response: ", track, "\n")
    #     cover = track['album']['images'][0]['url']
    #     covers[track['id']] = cover
    # # print("Cover Url: ", cover)
    
    # return covers
    return cover




@app.route("/ls-genres")
def getLikedCategories():
    genres = {}
    allGenres = set()
    holder = str()
    uncategorized = 0
    categorized = 0
    i=0
    j=0
    if 'access_token' not in session:
        return redirect('/login')
    else:
        token = session['access_token']
    
    if datetime.now().timestamp() >= session['expires_at']:
        print("Access Token Expired. Refreshing...")
        return redirect('/refresh-token')
    
    if token:
        try:
            sp = spotipy.Spotify(auth=token)
            liked_songs = sp.current_user_saved_tracks()
            size = liked_songs['total']
            print("Starting while loop\n")
            while i < size:
                # start_time = time.time()
                remaining = size - i
                batch_size = min(49, remaining)  # Ensure the batch size is not more than the remaining songs
                results = sp.current_user_saved_tracks(offset=i, limit=batch_size)
                i += batch_size
                k = 0
                # print("\nStarting For loop. Size of results is \n", results['total'] - i)
                # for songs in results['items']
                # print("Total number of things in RESULTS: ", len(results['items']))
                tracks = []
                for song in results['items']:
                    # print("--------------------------------------------------------------")
                    track = song['track']
                    track_name = track['name']
                    # print("\nSong found: ", track_name)
                    track_id = track['id']
                    # print("\nTrack ID found: ", track_id)
                    tracks.append(track_id)
                    track_artist = track['artists'][0]
                    # print("\nTrack artist simplified object found: ", track_artist)
                    artist_name = track_artist['name']
                    # print("\nTrack artist name found: ", artist_name)
                    artist_id = track_artist['id']
                    # print("\nTrack artist id found: ", artist_id)
                    holder = holder + artist_id + " "
                    k += 1
                    if k == 50 or song == results['items'][-1]:
                        if song == results['items'][-1]:
                            holder = holder + artist_id + " "
                            k-=1
                        holder = holder[:-1]
                        # print("Batch: ", holder)
                        idsInter = holder.split(" ")
                        # print("Number of IDs: ", len(idsInter), "\n")
                        ids = ",".join(idsInter)
                        holder = ""
                        # Spotify API endpoint to get artist information
                        # endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'
                        endpoint = f'https://api.spotify.com/v1/artists?ids={ids}'
                            # Set up headers with the access token
                        headers = {
                            'Authorization': f'Bearer {token}',
                        }
                        get_artist_response = requests.get(endpoint, headers=headers)

                        if get_artist_response.status_code == 429:
                            # #dump to json
                            with open('genres.json', 'w') as fp:
                                json.dump(genres, fp)

                            with open('allgenres.json', 'w') as fp:
                                json.dump(list(allGenres), fp)
                            # Rate limit exceeded, wait for some specified duration
                            retry_after = int(get_artist_response.headers['Retry-After'])
                            print(f"Rate limited. Waiting for {retry_after} seconds.")
                            time.sleep(retry_after)

                        if get_artist_response.status_code == 200:
                            artists = get_artist_response.json()
                            for artist in artists['artists']:
                                print("\nArtist: \n", artist['name'], "\n")
                            groupList = []
                            # print("groupList made")
                            # print("\nArtists Enumerated: \n", list(enumerate(artists['artists'])), "\n")
                            for index, artist in list(enumerate(artists['artists'])):
                                groupList.append((index, track_name, artist)) 
                        # artist = sp.artist(artist_id)
                            print("\nTrack artist object found \n")
                            # print("Group List: ", groupList)
                            for item in groupList:
                                # print("\nIndex: ", item[0])
                                if 0 <= item[0] < len(tracks):
                                    song_name = item[1]
                                    # print("Song: ", song_name)
                                    artist_genres = item[2] ['genres']
                                    # print("Artist ", item[2]['name']," Genres Found: \n", artist_genres)

                                    if artist_genres == []:
                                        uncategorized += 1
                                    else:
                                        categorized += 1

                                    if tracks[item[0]] not in genres:
                                        genres[track_id] = []
                                    genres[track_id] = track_name, item[2]['name'], artist_genres

                                    for genre in artist_genres:
                                        allGenres.add(genre)

                        else:
                            print(f"Error: {get_artist_response.status_code}, {get_artist_response.text}\nError on 181")
                        
                        tracks = []
                        k=0
                    j += 1
                    # print("\nTrack #",j)
                    # end_time = time.time()
                    # elapsed_time = end_time - start_time
                    # iterations_per_second = len(results['items']) / elapsed_time
                    # print(f"Iterations per second: {iterations_per_second}")
                    time.sleep(1/3)
            
            
            # #dump to json
            with open('genres.json', 'w') as fp:
                json.dump(genres, fp)
            allGenreList = list(allGenres)
            with open('allgenres.json', 'w') as fp:
                json.dump(list(allGenres), fp)

        except Exception as e:
            print(f"Error: {e}")
            return None
        session['categorized'] = categorized
        session['uncategorized'] = uncategorized
        return categorized, uncategorized, genres, allGenreList

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)