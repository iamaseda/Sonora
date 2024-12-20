import json

from flask import jsonify
import spotifyEnvironment as spotifyEnvironment
import spotipy.util as util
import spotipy
import requests
import time
import logout as logout
import secrets
from spotipy.oauth2 import SpotifyOAuth

client_id = spotifyEnvironment.client_id
client_secret = spotifyEnvironment.client_secret
redirect_uri = spotifyEnvironment.redirect_uri


scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public app-remote-control'
username = 'set your name'
state = secrets.token_urlsafe(16)
token = None

user_auth = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def login():
    #internally initiates OAuth 2.0 authorizatoin flow and retrieves necessary access token
    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,
                                    show_dialog=True)
    # url = 'https://accounts.spotify.com/authorize'
    # url += '?response_type=token'
    # url += '&client_id=' + requests.utils.quote(client_id)
    # url += '&scope=' + requests.utils.quote(scope)
    # url += '&redirect_uri=' + requests.utils.quote(redirect_uri)
    # url += '&state=' + requests.utils.quote(state)
    return token



def getLikedSongs(token):
    #get songs from Liked Songs
    songs = {}
    songInfo = []
    genres = {}
    i = 0
    
    if token:
        sp = spotipy.Spotify(auth=token)
        liked_songs = sp.current_user_saved_tracks()
        size = liked_songs['total']
        print("Number of liked songs: ", size)
        print("Liked_songs")
        print("Starting while loop\n")
        while i < size:
            # Results stores songs in clusters of 50
            results = sp.current_user_saved_tracks(offset=i, limit=50)
            songs[i] = results
            print("\n\nSongs Index: ", i)
            batch = songs[i]['items']
            for song in batch:
                print("\nSong: ", song['track']['name'], " by ", song['track']['artists'][0]['name'])
                track = song['track']['name']
                artist = song['track']['artists'][0]['name']
                songInfo.append((track, artist))
            i += 50
        print("\nSongs finished being parsed\n")
        return batch, songInfo
        # try:
        #     # Tracks stores all the tracks in the liked songs
        #     # tracks = liked_songs['items']
        #     # categories = set()
        #     # print(tracks)
        #     for _, song in songs.items():
        #         # Find the album within which a song can be found
        #         album = song['track']['album']
        #         if album:
        #             # Album information is available. Use its category
        #             genre = album.get('genres', [])
        #             # genre = album[0]
        #             # if category:
        #             #     categories.add(category['name'])
        #             print(genre, "\n")
        #             # if genre not in genres:
        #             #     genres[genre['name']] = []
        #             # genres[genre['name']].append(genre['id'])
        # except Exception as e:
        #     print(f"Error: {e}")
        #     return None

    #dump to json
    with open('songs.json', 'w') as fp:
        json.dump(songs, fp)


def getCategories(token):
    genres = {}
    allGenres = set()
    holder = str()
    uncategorized = 0
    categorized = 0
    i=0
    j=0
    if token:
        try:
            sp = spotipy.Spotify(auth=token)
            liked_songs = sp.current_user_saved_tracks()
            size = liked_songs['total']
            print("Starting while loop\n")
            while i < size:
                start_time = time.time()
                remaining = size - i
                batch_size = min(49, remaining)  # Ensure the batch size is not more than the remaining songs
                results = sp.current_user_saved_tracks(offset=i, limit=batch_size)
                i += batch_size
                k = 0
                print("\nStarting For loop. Size of results is \n", results['total'] - i)
                # for songs in results['items']
                print("Total number of things in RESULTS: ", len(results['items']))
                tracks = []
                for song in results['items']:
                    print("--------------------------------------------------------------")
                    track = song['track']
                    track_name = track['name']
                    print("\nSong found: ", track_name)
                    track_id = track['id']
                    # print("\nTrack ID found: ", track_id)
                    tracks.append(track_id)
                    track_artist = track['artists'][0]
                    # print("\nTrack artist simplified object found: ", track_artist)
                    artist_name = track_artist['name']
                    print("\nTrack artist name found: ", artist_name)
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
                        print("Number of IDs: ", len(idsInter), "\n")
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
                            print("groupList made")
                            # print("\nArtists Enumerated: \n", list(enumerate(artists['artists'])), "\n")
                            for index, artist in list(enumerate(artists['artists'])):
                                groupList.append((index, track_name, artist)) 
                        # artist = sp.artist(artist_id)
                            print("\nTrack artist object found \n")
                            print("Group List: ", groupList)
                            for item in groupList:
                                print("\nIndex: ", item[0])
                                if 0 <= item[0] < len(tracks):
                                    song_name = item[1]
                                    print("Song: ", song_name)
                                    artist_genres = item[2] ['genres']
                                    print("Artist ", item[2]['name']," Genres Found: \n", artist_genres)

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
                    print("\nTrack #",j)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    iterations_per_second = len(results['items']) / elapsed_time

                    print(f"Iterations per second: {iterations_per_second}")
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
        
        return categorized, uncategorized, genres, allGenreList
        


if __name__ == "__main__":

    getLikedSongs(login())
    # getCategories(logout.logout())