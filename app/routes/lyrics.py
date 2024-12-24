from flask import Blueprint, render_template, request

lyrics = Blueprint('lyrics', __name__)

@lyrics.route('/lyrics', methods= ['POST'])
def lyrics_page():
    user_input = request.form.get('user_input_url')
    return render_template('lyrics.html', user_input_url=user_input)
