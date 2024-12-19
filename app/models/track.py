from ..extensions import db
from datetime import datetime
import pytz

utc_now = datetime.now(pytz.utc)
# Model that represents the db table
class Track(db.Model):
    spotify_track_id = db.Column(db.String(50), primary_key=True)
    track_name = db.Column(db.String(100), nullable = False)
    track_artist = db.Column(db.String(100), nullable = False)
    track_image = db.Column(db.String(100))
    track_date_added = db.Column(db.DateTime, default=utc_now)

    #lyrics = db.relationship('Lyrics', back_populates='track', uselist=True) #* uncomment later when adding Lyrics

    def __init__(self, spotify_track_id, track_name, track_artist, track_image, track_date_added = utc_now):
        self.spotify_track_id = spotify_track_id
        self.track_name = track_name
        self.track_artist = track_artist
        self.track_image = track_image
        self.track_date_added = track_date_added

    def __repr__(self):
        return f"Track[('{self.spotify_track_id}'), ('{self.track_artist}'),  ('{self.track_name}'), ('{self.track_image}')]"