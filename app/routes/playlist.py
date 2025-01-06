import logging
from flask import Blueprint, render_template, request, jsonify
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
    #logging.debug(f"Tracks: %s", tracks)
    return render_template("playlist.html", spotify_playlist_id=spotify_playlist_id, playlist_name=playlist_name, playlist_image=playlist_image, tracks=tracks)


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