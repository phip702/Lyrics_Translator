import logging
from ..models.track import Track

def check_track_row_exists(track_id):
    track =  Track.query.filter_by(spotify_track_id=track_id).first()
    logging.debug(f"Does the track row for {track_id} already exist? --> {track is not None}")
    if track:
        return track.track_name, track.track_artist, track.track_image
    else:
        return None, None, None
    
def insert_row(db, Table_Instance):
    db.session.add(Table_Instance)
    db.session.commit()
    logging.debug("Row inserted")