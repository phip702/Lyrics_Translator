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

    lyrics = db.relationship('Lyrics', back_populates='track', uselist=False)

    def get_track_id(self):
        return self.spotify_track_id

    def get_track_name(self):
        return self.track_name
    
    def get_track_artist(self):
        return self.track_artist

    def get_track_image(self):
        return self.track_image

    def __init__(self, spotify_track_id, track_name, track_artist, track_image, track_date_added = None):
        self.spotify_track_id = spotify_track_id
        self.track_name = track_name
        self.track_artist = track_artist
        self.track_image = track_image
        if track_date_added:
            self.track_date_added = track_date_added
        else:
            self.track_date_added = utc_now

    def __repr__(self):
        return f"Track[('{self.spotify_track_id}'), ('{self.track_artist}'),  ('{self.track_name}'), ('{self.track_image}')]"
    
    def to_dict(self):
        """
        Convert the Track instance to a dictionary.
        This method can be used for serialization to JSON for rabbitmq
        """
        # Convert the instance to a dictionary, excluding non-serializable attributes
        return {
            'spotify_track_id': self.spotify_track_id,
            'track_name': self.track_name,
            'track_artist': self.track_artist,
            'track_image': self.track_image,
            'track_date_added': self.track_date_added.isoformat()  # Convert datetime to string
        }