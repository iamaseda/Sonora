import json
import spotifyEnvironment
import spotipy.util as util
import spotipy
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
    i = 0
    
    if token:
        sp1 = spotipy.Spotify(auth=token)
        liked_songs = sp1.current_user_saved_tracks()
        size = liked_songs['total']
        
        while i < size:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks(offset=i, limit=50)
            songs[i] = results
            i += 50
        try:
            tracks = liked_songs['items']
            categories = set()

            for song in tracks:
                category = song['track']['album'].get('category', None)
                if category:
                    categories.add(category['name'])
        except Exception as e:
            print(f"Error: {e}")
            return None

    #dump to json
    with open('songs.json', 'w') as fp:
        json.dump(songs, fp)

    with open('genres.json', 'w') as fp:
        json.dump(categories, fp)

def getCatefories():
    genres = {}
    holder = []
    if token:
        try:
            sp = spotipy.Spotify(auth=token)
            categories_response = sp.categories()
            categories = categories_response['categories']['items']
            sumCategories = len(categories)
            for i in range(sumCategories):
                genre_response = sp.categories(offset=i, limit=1)
                genre = genre_response['categories']['items'][0]
                if genre['name'] not in genres:
                    genres[genre['name']] = []
                genres[genre['name']].append(genre['id'])
                # holder.append(genre['name'])

            #dump to json
            with open('genres.json', 'w') as fp:
                json.dump(genres, fp)

            return categories
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":

    #getLikedSongs()
    getCatefories()