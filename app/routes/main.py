from flask import Blueprint, render_template, session, request, redirect, url_for
from ..services.genius import get_genius_auth_token  # Import relevant logic for the APIs
from dotenv import load_dotenv

load_dotenv()

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# Define the route for the home page
@main.route("/", methods=["GET", "POST"])
def home():
    # Authenticate the user to Genius if the token is not already in the session
    if 'genius_auth_token' not in session:
        genius_auth_token = get_genius_auth_token()
        session['genius_auth_token'] = genius_auth_token

    if request.method == 'POST':
        user_input_url = request.form.get("user_input_url")

        if '/track/' in user_input_url:
            spotify_track_id = user_input_url.split('/track/')[1].split('?')[0] #splits URL at /track/ and grabs the second element (so what comes after /track/)
            return redirect(url_for('track.track_page', spotify_track_id=spotify_track_id))
        
        return render_template('error.html', error_message="Invalid Spotify URL. Please enter a valid track URL.")
    
    return render_template('main.html')

