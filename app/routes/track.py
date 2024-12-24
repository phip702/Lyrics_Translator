import logging
from flask import Blueprint, render_template, request
from ..extensions import * #this import the db
from ..models.track import *
from ..handlers.model_handlers import *
from ..services.spotify import get_song_id_from_url, get_track_name_artist_image
from ..services.genius import get_song_lyrics
from ..handlers.lyrics_handler import get_translated_lyrics

track = Blueprint('track', __name__)

@track.route('/track/<spotify_track_id>', methods= ['GET']) #TODO: use spotify_track_id as part of the url, so /track/spotify_track_id; will need to POST this from main
def track_page(spotify_track_id):
    logging.debug((f"spotify_track_id: {spotify_track_id}"))

    track_name, track_artist, track_image = check_track_row_exists(spotify_track_id)

    if track_name is None: #get track info from Spotify and add to db
        track_name, track_artist, track_image = get_track_name_artist_image(spotify_track_id)
        if track_name == "Unknown Track": # 'Unknown Track' is what Spotify returns if it didn't find anything
            return render_template('error.html', error_message = f"Could not find info. Is your URL a valid URL? You entered: {user_input_url}")
    
        new_track = Track(spotify_track_id = str(spotify_track_id), track_name=track_name, track_artist=track_artist, track_image = track_image)
        insert_row(db, new_track)



    #TODO: port lyrics csv into the db, fetch the lyrics, then move on to making the app async then message queue
    original_lyrics, translated_lyrics, _ = check_lyrics_row_exists(spotify_track_id)
    #TODO: should original lyrics go through trim_lyrics() too?
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



    return render_template('track.html', track_name=track_name, track_artist=track_artist, track_image=track_image, zipped_lyrics=zipped_lyrics) 

#delete This is only for testing; don't forget to change the post method to go to 'lyrics' in main.html
