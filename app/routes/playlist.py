import logging
from flask import Blueprint, render_template
from ..services.spotify import get_playlist_name_image, get_playlist_tracks_name_artist_image

playlist = Blueprint('playlist', __name__)

@playlist.route('/playlist/<spotify_playlist_id>', methods= ['GET'])
def playlist_page(spotify_playlist_id):
    logging.debug((f"spotify_playlist_id: {spotify_playlist_id}"))
    playlist_name, playlist_image = get_playlist_name_image(spotify_playlist_id) #* (1)could async this
    logging.debug(f"Playlist: {playlist_name}; Image URL: {playlist_image}")
    if playlist_name == "Playlist Not Found":
        return render_template('error.html', error_message = f"Could not find info from Spotify. Is the playlist public?") 
    
    tracks = get_playlist_tracks_name_artist_image(spotify_playlist_id) #* (2)could async this
    logging.debug(f"Tracks: %s", tracks)
    return render_template("playlist.html", playlist_name=playlist_name, playlist_image=playlist_image, tracks=tracks)
    #TODO: make the html display the tracks