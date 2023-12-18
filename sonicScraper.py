import json
import spotifyEnvironment
import spotipy.util as util
import spotipy
import re

client_id = spotifyEnvironment.client_id
client_secret = spotifyEnvironment.client_secret
redirect_uri = spotifyEnvironment.redirect_uri



scope = 'user-library-read'
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

    #dump to json
    with open('songs.json', 'w') as fp:
        json.dump(songs, fp)



if __name__ == "__main__":

    getLikedSongs()