import pytest
import json
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

test_spotify_playlist_id = '4lvuWO8blWHWWGj3LfVzvD' #'Language Testing' playlist 
test_spotify_track_id = '278kSqsZIiYp8p3QjYAqa8' #'Ni Bien Ni Mal' also in 'Language Testing' playlist


@pytest.fixture
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()  # This assumes create_app initializes your Flask app
    yield app  # This will make the app available for the tests to use

@pytest.fixture
def db(app):
    # app is an instance of your Flask app, _db is the SQLAlchemy DB instance
    _db.app = app  # Attach app to the db instance
    with app.app_context():
        _db.create_all()  # Create tables for testing

    yield _db  # Yield control to the tests

    # Cleanup: close the session and drop all tables after each test
    _db.session.remove()  # Close the DB session
    _db.drop_all()  # Drop all tables after the test


#* ----------------- Main Route -----------------

def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Enter Spotify URL for a Song or Playlist" in response.data  # Check if the page contains the expected title
    assert b"Spotify URL:" in response.data  # Check if the form field is present
    assert b"Submit" in response.data  # Check if the submit button is present

def test_home_post_valid_track(client):
    valid_track_url = f"https://open.spotify.com/track/{test_spotify_track_id}" 
    response = client.post("/", data={"user_input_url": valid_track_url})

    assert response.status_code == 302  # 302 indicates a redirect
    assert response.location.endswith(f"/track/{test_spotify_track_id}") 

def test_home_post_valid_playlist(client):
    valid_playlist_url = f"https://open.spotify.com/playlist/{test_spotify_playlist_id}"
    response = client.post("/", data={"user_input_url": valid_playlist_url})

    assert response.status_code == 302
    assert response.location.endswith(f"/playlist/{test_spotify_playlist_id}") 

def test_home_post_invalid_url(client):
    invalid_url = "https://example.com/invalid_url"
    response = client.post("/", data={"user_input_url": invalid_url})

    # Check that the page returns the error template
    assert response.status_code == 200
    assert b"Invalid Spotify URL" in response.data  # Check for error message


#* ----------------- Track Route -----------------
def test_track_page(client):
    # Assuming the track is already in the database, we'll test for its page
    response = client.get(f"/track/{test_spotify_track_id}")
    print(response.data)
    assert response.status_code == 200
    assert b"NI BIEN NI MAL" in response.data
    assert b"Bad Bunny" in response.data 
    assert b"https://i.scdn.co/image/ab67616d0000b273519266cd05491a5b5bc22d1e" in response.data
    assert b"[Letra de &#34;NI BIEN NI MAL&#34;]" in response.data  # Check if the original lyrics are displayed
    assert b"[Lyrics of &#34;NI BIEN NI MAL&#34;]" in response.data  # Check if the translated lyrics are displayed


#* ----------------- Playlist Route -----------------
def test_playlist_track_navigation(client):
    # Ensure clicking on a track in the playlist navigates to the track page
    playlist_response = client.get(f"/playlist/{test_spotify_playlist_id}")
    assert playlist_response.status_code == 200

    # Can't simulate user actually clicking, but testing the reroute
    track_response = client.get(f"/track/{test_spotify_track_id}")
    assert track_response.status_code == 200
    assert b"NI BIEN NI MAL" in track_response.data  
    assert b"Bad Bunny" in track_response.data