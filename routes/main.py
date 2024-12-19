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
        user_input = request.form.get("user_input")
        return redirect(url_for('track.track_page', user_input=user_input))#delete
        #return redirect(url_for('lyrics.lyrics_page', user_input=user_input))
    
    return render_template('main.html')

