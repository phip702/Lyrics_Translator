import logging
from ..models import *

def check_track_row_exists(track_id):
    track =  Track.query.filter_by(spotify_track_id=track_id).first()
    logging.debug(f"Does the track row for {track_id} already exist? --> {track is not None}")
    if track:
        return track.track_name, track.track_artist, track.track_image
    else:
        return None, None, None
    
def check_lyrics_row_exists(track_id):
    lyrics = Lyrics.query.filter_by(spotify_track_id=track_id).first()
    logging.debug(f"Does the lyrics row for {track_id} already exist? {lyrics is not None}")
    if lyrics:
        return lyrics.original_lyrics, lyrics.translated_lyrics, lyrics.detected_language
    else:
        return None, None, None
    
def insert_row(db, Table_Instance):
    if type(Table_Instance) == Track:
        track = Track.query.filter_by(spotify_track_id=Table_Instance.spotify_track_id).first()
        if track:
            return #track already exists
        
    elif type(Table_Instance) == Lyrics:
        lyrics = Lyrics.query.filter_by(spotify_track_id=Table_Instance.spotify_track_id).first()
        if lyrics:
            return #track already exists

    # If row doesn't exist, insert it and log the success
    try:
        db.session.add(Table_Instance)
        db.session.commit()
        logging.debug(f"Row inserted successfully: {Table_Instance}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inserting row: {e}")
