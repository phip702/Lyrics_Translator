import logging
from datetime import datetime
import pytz
from sqlalchemy.orm import relationship


from .extensions import db


utc_now = datetime.now(pytz.utc)
# Model that represents the db table
class Track(db.Model):
    spotify_track_id = db.Column(db.String(50), primary_key=True)
    track_name = db.Column(db.String(100), nullable = False)
    track_artist = db.Column(db.String(100), nullable = False)
    track_image = db.Column(db.String(100))
    track_date_added = db.Column(db.DateTime, default=utc_now)

    lyrics = db.relationship('Lyrics', back_populates='track', uselist=True) 

    def __init__(self, spotify_track_id, track_name, track_artist, track_image):
        self.spotify_track_id = spotify_track_id
        self.track_name = track_name
        self.track_artist = track_artist
        self.track_image = track_image

    def __repr__(self):
        return f"Track[('{self.spotify_track_id}'), ('{self.track_artist}'),  ('{self.track_name}'), ('{self.track_image}')]"
    

class Lyrics(db.Model):
    spotify_track_id  = db.Column(db.String(50), db.ForeignKey('track.spotify_track_id'), primary_key = True)
    original_lyrics   = db.Column(db.String(10000), nullable = False) #*maps to VARCHAR so performance is fine. average songs <2500 characters
    translated_lyrics = db.Column(db.String(10000), nullable = False)
    detected_language = db.Column(db.String(8), nullable = False) #8 is longest language Azure string
    lyrics_date_added = db.Column(db.DateTime, default=utc_now)

    track = relationship("Track", back_populates = "lyrics", uselist=True)

    def __init__(self, spotify_track_id, original_lyrics, translated_lyrics, detected_language):
        self.spotify_track_id = spotify_track_id
        self.original_lyrics = original_lyrics
        self.translated_lyrics = translated_lyrics
        self.detected_language = detected_language

    def __repr__(self):
        return f"Lyrics[('{self.spotify_track_id}'), ('{self.detected_language}')]"