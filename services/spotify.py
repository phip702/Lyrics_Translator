import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
import logging

def get_song_id_from_url(url):
    idx = url.rfind('/') # finds the character position of the first '/' encountered searching from right to left
    spotify_track_id = url[idx +1:]
    logging.debug(f"Found spotify track id: {spotify_track_id}")
    return spotify_track_id #return everything to the right of the last '/' which should be the Spotify track ID

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

def get_track_info(spotify_track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{spotify_track_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    return json_result

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

if __name__ == "__main__":
    track_name, track_artist, track_image = get_track_name_artist_image("https://open.spotify.com/track/3HDYqfUZN3vToDnhqNsb6J?si=86e90d3add46498e") #24 Rosas test song
    print("\ntrack_name: ", track_name)
    print("\ntrack_artist: ", track_artist)
    print("\ntrack_image: ", track_image)