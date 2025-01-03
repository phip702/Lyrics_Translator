import pytest
import requests
from unittest.mock import patch
from app.services.azure_translate import (
    construct_translation_request,
    translate_text,
    map_translation_to_original,
    get_translation_for_original,
    azure_translate_load_credentials
)


@pytest.fixture
def mock_translation_map():
    return {
        "Sin ti no me va bien, tampoco me va mal (Yeah)": "Without you I don't do well, I don't do bad either (yes)",
        "Pase lo que pase no te voy a llamar": "No matter what happens, I'm not going to call you",
        "Ya yo me quité, tú nunca me va' a amar (Na)": "I've already taken off, you're never going to love me (Na)",
    }


@pytest.fixture
def mock_azure_response():
    return [
    {
        "detectedLanguage": {
            "language": "es",
            "score": 1.0
        },
        "translations": [
            {
                "text": "Without you I don't do well, I don't do bad either (yes)",
                "to": "en"
            }
        ]
    },
    {
        "detectedLanguage": {
            "language": "es",
            "score": 1.0
        },
        "translations": [
            {
                "text": "No matter what happens, I'm not going to call you",
                "to": "en"
            }
        ]
    },
    {
        "detectedLanguage": {
            "language": "es",
            "score": 0.99
        },
        "translations": [
            {
                "text": "I've already taken off, you're never going to love me (Na)",
                "to": "en"
            }
        ]
    }
]

def test_construct_translation_request():
    azure_translate_key, azure_translate_location = "fake_key", "fake_location"
    
    constructed_url, params, headers = construct_translation_request(azure_translate_key, azure_translate_location)
    
    assert constructed_url == "https://api.cognitive.microsofttranslator.com/translate"
    
    assert params["api-version"] == "3.0"
    assert params["from"] == [[]]  # auto-detect from language (empty list is the indicator for auto-detect)
    assert params["to"] == ['en']  # translation to English
    
    assert headers["Ocp-Apim-Subscription-Key"] == "fake_key"
    assert headers["Ocp-Apim-Subscription-Region"] == "fake_location"
    assert "X-ClientTraceId" in headers  # Check that a UUID is included in the header


@patch("requests.post") # Mock the request.post in translate_text() so the API isn't hit
def test_translate_text(mock_post, mock_azure_response):
    mock_post.return_value.json.return_value = mock_azure_response  # Mock the response
    
    azure_translate_key, azure_translate_location = "fake_key", "fake_location"
    constructed_url, params, headers = construct_translation_request(azure_translate_key, azure_translate_location)
    lyrics_set = {'Sin ti no me va bien, tampoco me va mal (Yeah)', 'Pase lo que pase no te voy a llamar', "Ya yo me quité, tú nunca me va' a amar (Na)"}
    
    response = translate_text(constructed_url, params, headers, lyrics_set)
    
    assert response == mock_azure_response



def test_map_translation_to_original(mock_translation_map, mock_azure_response):
    lyrics_list = list(mock_translation_map.keys())  # Convert the keys to a list to preserve the order; not an issue in prod
    translation_map = map_translation_to_original(lyrics_list, mock_azure_response)

    for original_lyrics in lyrics_list:
        expected_translation = mock_translation_map[original_lyrics]  # Get the expected translation from the map
        translated_lyrics = get_translation_for_original(translation_map, original_lyrics)

        #assert 1 == translated_lyrics, f"LYRICS SET: {lyrics_set}" #* Lyrics_Set is as expected
        #assert 2 == translated_lyrics, f"TRANSLATION MAP: {translation_map}"
        assert translated_lyrics == expected_translation, f"Mismatch for '{original_lyrics}': {translated_lyrics} != {expected_translation}"


# The function you're testing
def test_get_translation_for_original(mock_translation_map, original_line="Pase lo que pase no te voy a llamar"):
    translation_map = mock_translation_map
    translated_line = get_translation_for_original(translation_map, original_line)
    assert translated_line    



if __name__ == "__main__":
    pytest.main()
