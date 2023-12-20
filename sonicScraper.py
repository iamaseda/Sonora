import json
import spotifyEnvironment
import spotipy.util as util
import spotipy
import requests
import time
import re

client_id = spotifyEnvironment.client_id
client_secret = spotifyEnvironment.client_secret
redirect_uri = spotifyEnvironment.redirect_uri



scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public app-remote-control'
username = 'set your name' 

#internally initiates OAuth 2.0 authorizatoin flow and retrieves necessary access token
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

def getLikedSongs():
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

            # print(i+50,"\n")
            i += 50
        print("\nSongs finished being parsed\n")
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


def getCategories():
    genres = {}
    allGenres = set()
    holder = []
    i=0
    j=0
    if token:
        try:
            sp = spotipy.Spotify(auth=token)
            liked_songs = sp.current_user_saved_tracks()
            size = liked_songs['total']
            print("Starting while loop\n")
            while i < size:
                results = sp.current_user_saved_tracks(offset=i, limit=50)
                i += 50
                print("\nStarting For loop. Size of results is \n", results['total'] - i)
                for song in results['items']:
                    print("--------------------------------------------------------------")
                    track_name = song['track']['name']
                    print("\nSong found: ", track_name)
                    track_id = song['track']['id']
                    print("\nTrack ID found: ", track_id)
                    track_artist = song['track']['artists'][0]
                    print("\nTrack artist simplified object found: ", track_artist)
                    artist_name = track_artist['name']
                    print("\nTrack artist name found: ", artist_name)
                    artist_id = track_artist['id']
                    print("\nTrack artist id found: ", artist_id)
                    
                    # Spotify API endpoint to get artist information
                    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'
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
                        artist = get_artist_response.json()

                    # artist = sp.artist(artist_id)
                        print("\nTrack artist object found \n")

                        artist_genres = artist['genres']
                        print("\nTrack Artist Genres Found: \n", artist_genres)

                        if track_name not in genres:
                            genres[track_name] = []
                        genres[track_name] = artist_genres

                        for genre in artist_genres:
                            allGenres.add(genre)

                    else:
                        print(f"Error: {get_artist_response.status_code}, {get_artist_response.text}")
                    j += 1
                    print("\nTrack #",j)
                    # time.sleep(1)

            # #dump to json
            with open('genres.json', 'w') as fp:
                json.dump(genres, fp)

            with open('allgenres.json', 'w') as fp:
                json.dump(list(allGenres), fp)

        except Exception as e:
            print(f"Error: {e}")
            return None
        

if __name__ == "__main__":

    # getLikedSongs()
    getCategories()