from main import sonos_db
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, STRING, INTEGER

class User(sonos_db.Model):
    id = sonos_db.Column(sonos_db.Integer, primary_key=True) # profile.id
    username = sonos_db.Column(sonos_db.String(80), unique=True, nullable=False) # profile.display_name
    email = sonos_db.Column(sonos_db.String(120), unique=True, nullable=False) # profile.email
    uri = sonos_db.Column(sonos_db.String(225), unique=True, nullable=False) # profile.uri
    xcont = sonos_db.Column(sonos_db.ARRAY(BOOLEAN, BOOLEAN)) # profile.explicit_content (filter_enabled, filter_locked)
    external_url = sonos_db.Column(sonos_db.ARRAY(STRING)) # profile.external_urls
    followers = sonos_db.Column(sonos_db.ARRAY(STRING, INTEGER)) # (null href, total)
    url = sonos_db.Column(sonos_db.String(225)) # profile.href
    profilePic = sonos_db.Column(sonos_db.ARRAY(STRING, INTEGER, INTEGER)) # profile.images (URL, height, width)
    subscription = sonos_db.Column(sonos_db.String(225), nullable=False) # product
    type = sonos_db.Column(sonos_db.String(225), nullable=False) # profile.type

    def __repr__(self):
        return f'<User {self.username}>'
