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
        #return redirect(url_for('lyrics.lyrics_page', input_user_url=input_user_url)) #* use hard refresh to fix redirects not updating (Cmd + Shift + R)
        return redirect(url_for('track.track_page', input_user_url=user_input_url))#delete
    
    return render_template('main.html')

