# #!/usr/bin/env python3
# #line above this is a shebang line which specifies the path to the Python interpreter that should be used to execute the script
# import os
# from flask import Flask, request, render_template, session
# from app.spotify_api import get_track_name_artist_image, get_song_id_from_url
# from app.genius_api import get_genius_auth_token, get_song_lyrics
# from app.lyrics_handler import get_translated_lyrics
# import logging
# from dotenv import load_dotenv
# from app.plots import get_table_from_db, generate_bar_chart, generate_line_chart_lyrics, generate_fig_html
# from app.models_handlers import *
# from app.models import *
# from app.app_factory import create_app, db
# import time #delete later

# app = create_app()

# with app.app_context(): # Creates all tables tlhat do not already exist
#     #db.drop_all() #delete 
#     db.create_all()
# logging.debug(f"create all executed successfully")


# @app.route("/") # decorator indicates that main() should be run when the root URL 'swafinal.com/' of the application is accessed (when the application is visited in browser)
# def main(): 
#     # returns a string containing an HTML <form> with <input>. 
#     # The <form> ele specifies that the form data should be submitted to the server using POST and the action URL is '/lyrics
#     # the form also contains the submit button. when a user submits a form (input type = "submit"), it triggers and HTTP request

#     # authenticate the user to Genius
#     if 'genius_auth_token' not in session:
#         genius_auth_token = get_genius_auth_token()
#         session['genius_auth_token'] = genius_auth_token

#     return render_template('main.html')

# @app.route("/lyrics", methods=["POST"])
# def handle_lyrics_request():
#     #Optimize: existing track takes .30s for whole request; 3.3 for a new track
#     start_time = time.time() #delete 
#     track_url = request.form.get("user_input", "") #gets input "user_input" from the submitted form; "" returned if null
#     spotify_track_id = get_song_id_from_url(track_url)
        
#     track_name, track_artist, track_image = check_track_row_exists(spotify_track_id)
#     logging.debug(f"track_name: {track_name}")

#     if track_name is None: #get track info and add to db
#         track_name, track_artist, track_image = get_track_name_artist_image(spotify_track_id)
#         if track_name == "Unknown Track": # 'Unknown Track' is what Spotify returns if it didn't find anything
#             return render_template('error.html', error_message = f"Could not find info. Is your URL a valid URL? You entered: {track_url}")
    
#         new_track = Track(spotify_track_id = str(spotify_track_id), track_name=track_name, track_artist=track_artist, track_image = track_image)
#         insert_row(db, new_track)

#     mid_time = time.time() #delete   
#     original_lyrics, translated_lyrics, _ = check_lyrics_row_exists(spotify_track_id)
#     if original_lyrics is None: #get lyrics and add to db
#         original_lyrics = get_song_lyrics(track_name, track_artist)
#         logging.debug(f"Original lyrics: {original_lyrics}")
#         if original_lyrics == "Could not find lyrics":
#             return render_template('error.html', error_message = original_lyrics) # Returning here prevents inserting "Could not find lyrics" into Lyrics table
        
#         logging.debug("First 3 Lines of Original Lyrics:\n{}".format('\n'.join(original_lyrics.splitlines()[:3])))
#         translated_lyrics, detected_language = get_translated_lyrics(original_lyrics)
#         logging.debug("First 3 lines of Translated lyrics:\n{}".format('\n'.join(translated_lyrics.splitlines()[:3])))
#         new_lyrics = Lyrics(spotify_track_id = spotify_track_id, original_lyrics = original_lyrics, translated_lyrics = translated_lyrics, detected_language = detected_language)
#         insert_row(db, new_lyrics) #TODO: don't want to insert 'Couldn't get lyrics' or the like

#     zipped_lyrics = zip(original_lyrics.split('\n'), translated_lyrics.split('\n'))
#     end_time = time.time() # delete
#     logging.debug(f"to_mid     = {mid_time - start_time}")
#     logging.debug(f"mid_to_end = {end_time - mid_time}")
#     logging.debug(f"total_time = {end_time - start_time}")

#     return render_template('track_info_lyrics_translated.html', track_name=track_name, track_artist=track_artist, 
#                            track_image=track_image, zipped_lyrics= zipped_lyrics)

# @app.route("/user_analytics")
# def user_analytics():
#     logging.debug(f"query all: {db.session.query(Track).all()}") #*can i access db here? i can import
#     df = get_table_from_db(db, Lyrics)

#     bargraph_fig = generate_bar_chart(df, "detected_language")
#     linegraph_fig = generate_line_chart_lyrics(df, "detected_language")

#     bargraph_html = generate_fig_html(bargraph_fig)
#     linegraph_html = generate_fig_html(linegraph_fig)

#     return render_template('user_analytics.html', plot1_html = bargraph_html, plot2_html = linegraph_html)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5001)) # tells Flask to look for the PORT variable assigned by Heroku else use local port 5001
#     app.run(host='0.0.0.0', port = port) # 0.0.0.0 means run on all addresses

# #TODO: remove .env from Github and put them into Heroku instead so they remain hidden
