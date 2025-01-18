import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..services.spotify import get_playlist_name_image, get_playlist_tracks_name_artist_image
from prometheus_client import Counter

playlist = Blueprint('playlist', __name__)

http_requests_playlist = Counter('http_requests_playlist', 'Number of visits to the root URL', ['route'])

@playlist.route('/playlist/<spotify_playlist_id>', methods= ['GET'])
def playlist_page(spotify_playlist_id):
    http_requests_playlist.labels(route='/').inc() #increment
    logging.debug((f"spotify_playlist_id: {spotify_playlist_id}"))
    playlist_name, playlist_image = get_playlist_name_image(spotify_playlist_id) #* (1)could async this
    logging.debug(f"Playlist: {playlist_name}; Image URL: {playlist_image}")
    if playlist_name == "Playlist Not Found":
        return render_template('error.html', error_message = f"Could not find info from Spotify. Is the playlist public?") 
    
    tracks = get_playlist_tracks_name_artist_image(spotify_playlist_id) #* (2)could async this
    #logging.debug(f"Tracks: %s", tracks)
    return render_template("playlist.html", spotify_playlist_id=spotify_playlist_id, playlist_name=playlist_name, playlist_image=playlist_image, tracks=tracks)

#= This is for the sidenav user inputs to reroute to the normal playlist URL
@playlist.route('/redirect_to_playlist', methods=['POST'])
def redirect_to_playlist():
    user_input_url = request.form.get('user_input_url', '').strip()
    
    # Validate the input and extract the playlist ID
    if '/playlist/' in user_input_url:
        try:
            spotify_playlist_id = user_input_url.split('/playlist/')[1].split('?')[0]
            return redirect(url_for('playlist.playlist_page', spotify_playlist_id=spotify_playlist_id))
        except IndexError:
            logging.error(f"Malformed Spotify Playlist URL: {user_input_url}")
            return render_template('error.html', error_message="Invalid Spotify Playlist URL.")
    else:
        logging.error(f"Invalid URL entered: {user_input_url}")
        return render_template('error.html', error_message="URL does not contain a valid Spotify Playlist.")



@playlist.route('/api/fetch_tracks/<spotify_playlist_id>', methods=['GET'])
def fetch_tracks_api(spotify_playlist_id):
    """
    Internal API endpoint to fetch tracks from a Spotify playlist.
    Supports pagination to fetch additional tracks.
    """
    # Get the `offset` parameter from the request, default to 0
    offset = int(request.args.get('offset', 50))

    logging.debug(f"Fetching tracks for Playlist ID: {spotify_playlist_id} with offset: {offset}")

    # Fetch the tracks with pagination
    tracks = get_playlist_tracks_name_artist_image(spotify_playlist_id, offset)

    # Return the tracks as a JSON response
    if not tracks:
        return jsonify({'error': 'Could not fetch tracks'}), 400
    
    # Filter out only the necessary fields (name, artist, image) from each track
    filtered_tracks = [
        {
            'spotify_track_id': track.spotify_track_id,
            'track_name': track.track_name,
            'track_artist': track.track_artist,
            'track_image': track.track_image
        }
        for track in tracks
    ]

    return jsonify(filtered_tracks)