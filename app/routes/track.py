import logging
from flask import Blueprint, render_template, request
from ..services.spotify import get_song_id_from_url, get_track_name_artist_image
from ..handlers.model_handlers import check_track_row_exists, insert_row
from ..models.track import Track
from ..extensions import * #this import the db

track = Blueprint('track', __name__)

@track.route('/track', methods= ['POST'])
def track_page():
    user_input_url = request.form.get('user_input_url')
    spotify_track_id = get_song_id_from_url(user_input_url)
    logging.debug((f"spotify_track_id: {spotify_track_id}"))

    track_name, track_artist, track_image = check_track_row_exists(spotify_track_id)

    if track_name is None: #get track info from Spotify and add to db
        track_name, track_artist, track_image = get_track_name_artist_image(spotify_track_id)
        if track_name == "Unknown Track": # 'Unknown Track' is what Spotify returns if it didn't find anything
            return render_template('error.html', error_message = f"Could not find info. Is your URL a valid URL? You entered: {user_input_url}")
    
        new_track = Track(spotify_track_id = str(spotify_track_id), track_name=track_name, track_artist=track_artist, track_image = track_image)
        insert_row(db, new_track)






    return render_template('track.html', track_name=track_name, track_artist=track_artist, track_image=track_image)

#delete This is only for testing; don't forget to change the post method to go to 'lyrics' in main.html
