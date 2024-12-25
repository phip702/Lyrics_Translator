import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
import logging
from ..models import Track

#TODO: will need to get refresh tokens or get new ones; could be useful to add an if statement to see if we already have a good URL?
def get_token():
    load_dotenv(dotenv_path="./.env") #loads environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_string = client_id+":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    return(json_result['access_token']) # dict with keys: {access_token, tooken_type, expires_in}

def get_auth_header(token):
    return {"Authorization": "Bearer "  + token}


#* ----------------- TRACK FUNCTIONS -----------------
# def get_song_id_from_url(url):
#     idx = url.rfind('/') # finds the character position of the first '/' encountered searching from right to left
#     spotify_track_id = url[idx +1:]
#     logging.debug(f"Found spotify track id: {spotify_track_id}")
#     return spotify_track_id #return everything to the right of the last '/' which should be the Spotify track ID
#Delete?

def get_track_info(spotify_track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{spotify_track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code != 200: #if status code unsuccesful
        logging.error(f"Error fetching track info: {result.status_code} - {result.text}")
        return None

    try:
        # Try to parse the response as JSON
        json_result = result.json()
        return json_result
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the response: {result.text}")
        return None

def get_track_name(track_json_result):
    return track_json_result.get('name', 'Unknown Track')

def get_track_artist(track_json_result):
    artists = track_json_result.get('artists', [])
    if artists:
        return artists[0].get('name', 'Unknown Artist')
    return 'Unknown Artist'

def get_track_image(track_json_result): #this returns the image url not the image itself
    album_images = track_json_result.get('album', {}).get('images', [])
    if album_images:
        return album_images[0].get('url', 'No Image Available') #the first image should be the highest definition
    return 'No Image Available'

def get_track_name_artist_image(spotify_track_id): #todo: change this to take in song_id argument instead
    token = get_token()
    track_json_result = get_track_info(spotify_track_id, token)
    track_name = get_track_name(track_json_result)
    track_artist = get_track_artist(track_json_result)
    track_image = get_track_image(track_json_result)
    logging.debug(f"Spotify's Track Name: {track_name}, Artist: {track_artist}, Image URL: {track_image}")
    return track_name, track_artist, track_image



#* ----------------- PLAYLIST FUNCTIONS -----------------
def get_playlist_info(spotify_playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    logging.debug(f"get_playlist_info playlist id: {spotify_playlist_id}")
    if result.status_code != 200: #if status code unsuccesful
        logging.error(f"Error fetching playlist info: {result.status_code} - {result.text}") #* The playlist may not be public --> Error fetching playlist info: 404 - {"error": {"status": 404, "message": "Resource not found" } }
        return None

    try:
        # Try to parse the response as JSON
        json_result = result.json()
        #logging.debug(f"get_playlist_info result: {json_result}")
        return json_result
    
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the response: {result.text}")
        return None

def get_playlist_name(playlist_json_result):
    return playlist_json_result.get('name', 'Unknown Playlist Name')

def get_playlist_image(playlist_json_result):
    playlist_image = playlist_json_result.get('images', [])
    if playlist_image:
        return playlist_image[0].get('url', 'No Image Available') #the first image should be the highest definition
    return 'No Image Available'

def get_playlist_name_image(spotify_playlist_id):
    token = get_token()
    playlist_json_result = get_playlist_info(spotify_playlist_id, token)
    if not playlist_json_result:
        return "Playlist Not Found", "Playlist Not Found"
    playlist_name = get_playlist_name(playlist_json_result)
    playlist_image = get_playlist_image(playlist_json_result)
    logging.debug(f"Spotify Playlist Name: {playlist_name}, Image URL: {playlist_image}")
    return playlist_name, playlist_image



#* ----------------- PLAYLIST TRACK FUNCTIONS -----------------
def get_playlist_tracks_info(spotify_playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)

    if result.status_code != 200: #if status code unsuccesful
        logging.error(f"Error fetching playlist info: {result.status_code} - {result.text}")
        return None

    try:
        # Try to parse the response as JSON
        json_result = result.json()
        return json_result
    
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the response: {result.text}")
        return None
    
def get_playlist_tracks_name_artist_image(playlist_tracks_json):
    items = playlist_tracks_json.get('items', "No Items")
    tracks = []
    for item in items:
        track = item.get('track', [])
        track_id = track.get('id', "Track ID not found")
        track_name = get_track_name(track)
        track_artist = get_track_artist(track)
        track_image = get_track_image(track)
        new_track = Track(spotify_track_id=str(track_id), track_name=track_name, track_artist=track_artist, track_image = track_image)
        logging.debug(f"Playlist Track Class created: %s", new_track)
        tracks.append(new_track)
        #TODO: make the messaging queue add these to committs for the db
    return tracks



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    track_name, track_artist, track_image = get_track_name_artist_image("3HDYqfUZN3vToDnhqNsb6J?si=86e90d3add46498e") #24 Rosas test songß

    playlist_name, playlist_image = get_playlist_name_image("4lvuWO8blWHWWGj3LfVzvD")
    token = get_token()
    playlist_tracks_json = get_playlist_tracks_info("4lvuWO8blWHWWGj3LfVzvD", token)
    playlist_track_info = get_playlist_tracks_name_artist_image(playlist_tracks_json)
