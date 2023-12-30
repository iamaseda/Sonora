import os

os.environ['SPOTIPY_CLIENT_ID'] = '6a6f0739de4345f6ab1abb31eae509c9'
os.environ['SPOTIPY_CLIENT_SECRET'] = '10d5a4ab905540b89f6a77cd031c029a'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

# Use the environment variables to provide client ID, client secret, and redirect URI
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
