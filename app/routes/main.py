from flask import Blueprint, render_template, session, request, redirect, url_for
from ..services.genius import get_genius_auth_token  # Import relevant logic for the APIs
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

load_dotenv()

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

def strip_query_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Create a new URL without the query parameters
    stripped_url = urlunparse(parsed_url._replace(query=''))
    
    return stripped_url

# Define the route for the home page
@main.route("/", methods=["GET", "POST"])
def home():
    # Authenticate the user to Genius if the token is not already in the session
    if 'genius_auth_token' not in session:
        genius_auth_token = get_genius_auth_token()
        session['genius_auth_token'] = genius_auth_token

    if request.method == 'POST':
        user_input_url = request.form.get("user_input_url")
        user_input_url_stripped = strip_query_from_url(user_input_url)

        if '/track/' in user_input_url_stripped:
            spotify_track_id = user_input_url_stripped.split('/track/')[1].split('?')[0] #splits URL at /track/ and grabs the second element (so what comes after /track/)
            return redirect(url_for('track.track_page', spotify_track_id=spotify_track_id))
    
        elif '/playlist/' in user_input_url_stripped:
            spotify_playlist_id = user_input_url_stripped.split('/playlist/')[1].split('?')[0]
            return redirect(url_for('playlist.playlist_page', spotify_playlist_id=spotify_playlist_id))
                                    
        
        else:
            return render_template('error.html', error_message= f"Invalid Spotify URL. Please enter a valid URL. You entered: {user_input_url}")
    
    return render_template('main.html')