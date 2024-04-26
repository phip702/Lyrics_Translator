import unittest
import unittest.mock as mock
from app.views import get_song_lyrics
from app.genius_api import get_genius_auth_token, get_song_lyrics
import logging


class TestSongLyrics(unittest.TestCase):
    
    @mock.patch("app.views.get_song_lyrics")
    def test_get_song_lyrics(self, mock_func):
        
        genius_auth_token = get_genius_auth_token() #need token to access Genius API

        #set variables for testing
        tempo_url = "https://open.spotify.com/track/7icIDep1Jr3oJdgJSGsdnM?si=ba55107e4f25442c"
        tempo_track_artist = "Marshmello"
        tempo_track_name = "Tempo"
        with open("./test_data/tempo.txt") as file:
                expected_lyrics = file.read()



        mock_func.return_value = expected_lyrics

        actual_lyrics = get_song_lyrics(tempo_track_name, tempo_track_artist)

        self.assertEqual(actual_lyrics, expected_lyrics, 
                         msg = f"The lyrics returned by get_song_lyrics do not match the expected lyrics. returned: {actual_lyrics}")
        print("Great Success!")


if __name__ == "__main__":
    unittest.main()