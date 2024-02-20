# from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, VARCHAR, INTEGER
from app import sonos_db
from flask_sqlalchemy import SQLAlchemy

class User(sonos_db.Model):
    id = sonos_db.Column(INTEGER, primary_key=True, unique=True) # profile.id
    username = sonos_db.Column(VARCHAR(80), unique=True, nullable=False) # profile.display_name
    email = sonos_db.Column(VARCHAR(120), unique=True, nullable=False) # profile.email
    uri = sonos_db.Column(VARCHAR(225), unique=True, nullable=False) # profile.uri
    xcont = sonos_db.Column(ARRAY(BOOLEAN, BOOLEAN)) # profile.explicit_content (filter_enabled, filter_locked)
    external_url = sonos_db.Column(ARRAY(VARCHAR)) # profile.external_urls
    followers = sonos_db.Column(ARRAY((VARCHAR, INTEGER))) # (null href, total)
    url = sonos_db.Column(VARCHAR(225)) # profile.href
    profilePic = sonos_db.Column(ARRAY((VARCHAR, INTEGER, INTEGER))) # profile.images (URL, height, width)
    subscription = sonos_db.Column(VARCHAR(225), nullable=False) # product
    type = sonos_db.Column(VARCHAR(225), nullable=False) # profile.type

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

class Track(sonos_db.Model):
    spotify_id = sonos_db.Column(INTEGER, primary_key=True, unique=True) # spotify track id
    uid = sonos_db.Column(INTEGER, sonos_db.ForeignKey('User.id'))
    title = sonos_db.Column(VARCHAR(100), nullable=False) # spotify track title
    genretags = sonos_db.Column(ARRAY(VARCHAR(225))) # cynaite track genre(s)
    subgenretags = sonos_db.Column(VARCHAR(225)) # cyanite track subgenre(s)
    moodtags = sonos_db.Column(ARRAY(VARCHAR(50))) # cyanite track mood(s)

    def __init__(self, spotify_id, title):
        self.spotify_id = spotify_id
        self.title = title

    def __repr__(self):
        return f'<Track: {self.title}>'
    
