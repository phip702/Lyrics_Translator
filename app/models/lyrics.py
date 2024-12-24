from ..extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship
import pytz

utc_now = datetime.now(pytz.utc)

class Lyrics(db.Model):
    spotify_track_id  = db.Column(db.String(50), db.ForeignKey('track.spotify_track_id'), primary_key = True)
    original_lyrics   = db.Column(db.String(10000), nullable = False) #*maps to VARCHAR so performance is fine. average songs <2500 characters
    translated_lyrics = db.Column(db.String(10000), nullable = False)
    detected_language = db.Column(db.String(8), nullable = False) #8 is longest language Azure string
    lyrics_date_added = db.Column(db.DateTime, default=utc_now)

    track = relationship("Track", back_populates = "lyrics", uselist=False) #each track will only have one lyrics

    def __init__(self, spotify_track_id, original_lyrics, translated_lyrics, detected_language, lyrics_date_added=None):
        self.spotify_track_id = spotify_track_id
        self.original_lyrics = original_lyrics
        self.translated_lyrics = translated_lyrics
        self.detected_language = detected_language
        if lyrics_date_added:
            self.lyrics_date_added=lyrics_date_added
        else:
            self.lyrics_date_added = utc_now

    def __repr__(self):
        return f"Lyrics[('{self.spotify_track_id}'), ('{self.detected_language}')]"