import unittest
#from flask import request
from dotenv import load_dotenv
import sys
import os
import logging
sys.path.append('../') # Run from one folder up
module_pwd = os.path.dirname(os.path.abspath(__file__))

logging.debug("Module's PWD:", sys.path)
from run import app
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def load_test_lyrics(filename):
    with open(filename, 'r') as file:
        lyrics = file.read()
        return lyrics
    

class TestLyricsTemplate(unittest.TestCase):

    def test_lyrics_template_format(self):
        with app.test_request_context('lyrics', method = 'POST', data = {'user_input': 'track_url'}):
            original_lyrics = load_test_lyrics("./test_data/24_Rosas.txt")
            translated_lyrics = load_test_lyrics("./test_data/24_Rosas_translated_lyrics.txt")

            #zip doesn't work in Jinja, have to pass the object in
            zipped_lyrics = zip(original_lyrics.split('\n'), translated_lyrics.split('\n'))

        rendered_template = app.jinja_env.get_template('track_info_lyrics_translated.html').render(
            track_name = "24 Rosas",
            track_artist = "Aitana",
            track_image = "https://i.scdn.co/image/ab67616d0000b2732f74dd3a7c4ec82b58479b56",
            zipped_lyrics = zipped_lyrics
        )

        #write results to .html to see first-hand
        with open("./tests/rendered_track_info_lyrics_translated.html", "w") as html_file:
                html_file.write(rendered_template)

        # Check if the template renders the lyrics correctly
        self.assertIn("Track Information", rendered_template)
        self.assertIn("Original Lyrics", rendered_template)
        self.assertIn("Translated Lyrics", rendered_template)
        for original_line, translated_line in zipped_lyrics:
            self.assertIn(original_line, rendered_template)
            self.assertIn(translated_line, rendered_template)

if __name__ == "__main__":
    unittest.main()