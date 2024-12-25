import logging
from flask import Blueprint, render_template, request
from ..extensions import * #this import the db
from ..models.track import *
from ..handlers.model_handlers import *
from ..services.spotify import get_track_name_artist_image
from ..services.genius import get_song_lyrics
from ..handlers.lyrics_handler import get_translated_lyrics

import time #delete later

track = Blueprint('track', __name__)

@track.route('/track/<spotify_track_id>', methods= ['GET'])
def track_page(spotify_track_id):
    start_time = time.time() #delete 
    logging.debug((f"spotify_track_id: {spotify_track_id}"))

    track_name, track_artist, track_image = check_track_row_exists(spotify_track_id)

    if track_name is None: #get track info from Spotify and add to db
        track_name, track_artist, track_image = get_track_name_artist_image(spotify_track_id)
        if track_name == "Unknown Track": # 'Unknown Track' is what Spotify returns if it didn't find anything
            return render_template('error.html', error_message = f"Could not find info from Spotify") #if reaches this point, the user should have passed a proper track URL
    
        new_track = Track(spotify_track_id = str(spotify_track_id), track_name=track_name, track_artist=track_artist, track_image = track_image)
        insert_row(db, new_track)

    mid_time = time.time() #delete  
    original_lyrics, translated_lyrics, _ = check_lyrics_row_exists(spotify_track_id)
    if original_lyrics is None: # get lyrics and add to db
        original_lyrics = get_song_lyrics(track_name, track_artist)
        logging.debug(f"Original lyrics: {original_lyrics}")
        if original_lyrics == "Could not find lyrics":
            return render_template('error.html', error_message = original_lyrics) # Returning here prevents inserting "Could not find lyrics" into Lyrics table
        
        logging.debug("First 3 Lines of Original Lyrics:\n{}".format('\n'.join(original_lyrics.splitlines()[:3])))
        translated_lyrics, detected_language = get_translated_lyrics(original_lyrics)
        logging.debug("First 3 lines of Translated lyrics:\n{}".format('\n'.join(translated_lyrics.splitlines()[:3])))
        new_lyrics = Lyrics(spotify_track_id = spotify_track_id, original_lyrics = original_lyrics, translated_lyrics = translated_lyrics, detected_language = detected_language)
        insert_row(db, new_lyrics) #TODO: don't want to insert 'Couldn't get lyrics' or the like

    zipped_lyrics = zip(original_lyrics.split('\n'), translated_lyrics.split('\n'))


    end_time = time.time() # delete
    logging.debug(f"to_mid     = {mid_time - start_time}")
    logging.debug(f"mid_to_end = {end_time - mid_time}") #* 85%ish of the time taken is done here
    logging.debug(f"total_time = {end_time - start_time}")

    return render_template('track.html', track_name=track_name, track_artist=track_artist, track_image=track_image, zipped_lyrics=zipped_lyrics) 

#TODO: async then message queue
#TODO: testing
#TODO: analytics --just use my old artifact, don't do anything more
#TODO: push to Heroku
#TODO: continuous integration?
#TODO: continuous delivery?
#TODO: production monitoring instrumenting
#TODO: front end
#TODO: make genius api call ignore 'romanized' versions