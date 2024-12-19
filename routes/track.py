
from flask import Blueprint, render_template, request

track = Blueprint('track', __name__)

@track.route('/track', methods= ['POST'])
def track_page():
    user_input = request.form.get('user_input')
    return render_template('track.html', user_input=user_input)

#delete This is only for testing; don't forget to change the post method to go to 'lyrics' in main.html
