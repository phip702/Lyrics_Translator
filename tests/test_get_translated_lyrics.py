import json
from app.lyrics_handler import get_translated_lyrics
import unittest.mock as mock
import unittest

def load_translation_response(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def load_test_lyrics(filename):
    with open(filename, 'r') as file:
        lyrics = file.read()
        return lyrics

def compare_strings_line_by_line(returned, expected):
    lines1 = returned.split('\n')
    lines2 = expected.split('\n')
    
    # Find the maximum number of lines between the two strings
    max_lines = max(len(lines1), len(lines2))
    
    # Compare line by line
    for i in range(max_lines):
        if i < len(lines1) and i < len(lines2):
            if lines1[i] != lines2[i]:
                print(f"Difference found at line {i + 1}:")
                print(f"  returned : {lines1[i]}")
                print(f"  expected : {lines2[i]}")
        elif i < len(lines1):
            print(f"Extra line found in string 1 at line {i + 1}: {lines1[i]}")
        else:
            print(f"Extra line found in string 2 at line {i + 1}: {lines2[i]}")



class TestGetTranslatedLyrics(unittest.TestCase):

    @mock.patch("app.lyrics_handler")
    def test_get_translated_lyrics(self, mock_create_translation_map):
        translation_response = load_translation_response("./test_data/24_Rosas_translation_response.JSON")
        mock_create_translation_map.return_value = (translation_response, "es")
        lyrics = load_test_lyrics("./test_data/24_Rosas.txt")
        expected_translated_lyrics = load_test_lyrics("./test_data/24_Rosas_translated_lyrics.txt")

        translated_lyrics, detected_language = get_translated_lyrics(lyrics)

        self.assertEqual(translated_lyrics, expected_translated_lyrics,
                         msg = f"The translated lyrics do not match the expected translated lyrics.\ndifferences: {compare_strings_line_by_line(translated_lyrics, expected_translated_lyrics)}")
        self.assertEqual(detected_language, "es",
                         msg = "The detected language does not match the expected detected language.")
        

if __name__ == "__main__":
    unittest.main()