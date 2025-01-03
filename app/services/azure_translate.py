# the Azure translate API gives the same 2M free characters to translate but it then only costs $10/million vs AWS's and Papago's $15/Million

import requests, uuid, json
import os
from dotenv import load_dotenv
import logging
from collections import Counter


def azure_translate_load_credentials():
    load_dotenv()
    azure_translate_key = os.getenv("AZURE__TRANSLATE_KEY")
    azure_translate_location = os.getenv("AZURE_TRANSLATE_LOCATION")
    return azure_translate_key, azure_translate_location

def construct_translation_request(azure_translate_key, azure_translate_location, from_lang = [], to_lang = 'en'):
    ''' This function constructs the translation request info, excluding the actual text to be translated.
        The from lang will default to auto detect.  
        #optimize: This could possibly be sped up by having the user set the from_lang. 
            Tests would need to be ran to see how much faster specifying the language is vs detecting it. 
            However, letting auto detect run allows the translator to do multiple languages for songs with multiple languages!
            For this reason, from_lang is set to be detected.
    ''' 
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': [from_lang], #empty list is auto-detect; link to language codes: https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
        'to': [to_lang] #can request multiple languages as a list
    }

    headers = {
        'Ocp-Apim-Subscription-Key': azure_translate_key,
        'Ocp-Apim-Subscription-Region': azure_translate_location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    return constructed_url, params, headers



def translate_text(constructed_url, params, headers, text_set):
    ''' This function actually contacts the translate API.'''
    body = [{'text': text} for text in text_set]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json() #*returns in order
    print(f"TRANSLATE_TEXT RESPONSE: {response}")
    return response


def print_response(response): #delete later; just formats nicely
    print(json.dumps(response, sort_keys = True, ensure_ascii=False, indent=4, separators=(',', ': ')))


def map_translation_to_original(lyrics_set_list, response):
    ''' 
    This function takes a lyrics set and the translation response and will create a map of a line of original lyrics to a line of translated lyrics.
    '''
    translation_map = {}
    for idx, translation_info in enumerate(response):
        translated_lyrics = translation_info['translations'][0]['text']
        original_lyrics = lyrics_set_list[idx]
        translation_map[original_lyrics] = translated_lyrics
    
    return translation_map

def get_translation_for_original(translation_map, original_line):
    ''' This uses the translation_map to get the translated line for an original line.'''
    return translation_map.get(original_line, "Translation not found")

def get_detected_language(azure_response):
    '''This grabs the first non-english language that has a certain amount of lines with a perfect score of 1.0, meaning Azure is certain it's that language. This prevents errors of grabbing a wrong/accidental language. Else assume the song was just in English'''
    
    language_counter = Counter()
    score_threshold = 1.0
    lines_past_score_threshold = 3

    # Loop through each item in the JSON data, getting a count of lines for each detected language at or above score threshold
    for item in azure_response:
        # Get the detected language from each item
        detected_language = item['detectedLanguage']['language']
        score = item['detectedLanguage']['score']
        
        if score >= score_threshold:
            language_counter[detected_language] += 1

    for lang, count in language_counter.items():
        if lang != 'en' and count >= lines_past_score_threshold:
            logging.debug(f"Detected Language: {lang}")
            return lang
    
    else:
        return "en"

def create_translation_map(lyrics_set_list):
    '''
    This function encompasses the entirety of this module. It will connect to Azure, make translations from the lyrics_set, 
    and make and return a translation_map.
    '''
    azure_translate_key, azure_translate_location = azure_translate_load_credentials()
    constructed_url, params, headers = construct_translation_request(azure_translate_key, azure_translate_location)
    response = translate_text(constructed_url, params, headers, lyrics_set_list)
    translation_map = map_translation_to_original(lyrics_set_list, response)
    detected_language = get_detected_language(response)
    return translation_map, detected_language


#* run the file to see it in action
#* translation respones are not 100% consistent given the same input lyrics
if __name__ == "__main__":
    azure_translate_key, azure_translate_location = azure_translate_load_credentials()
    constructed_url, params, headers = construct_translation_request(azure_translate_key, azure_translate_location)

    mock_translation_map = {
        "Sin ti no me va bien, tampoco me va mal (Yeah)": "Without you I don't do well, I don't do bad either (yes)",
        "Pase lo que pase no te voy a llamar": "No matter what happens, I'm not going to call you",
        "Ya yo me quité, tú nunca me va' a amar (Na)": "I've already taken off, you're never going to love me (Na)",
    }
    lyrics_list = list(mock_translation_map.keys())

    response = translate_text(constructed_url, params, headers, lyrics_list)
    print_response(response)

    translation_map = map_translation_to_original(lyrics_list, response)

    for line in lyrics_list:
        print(f"Original Line: {line}; Translated Line: {get_translation_for_original(translation_map, line)}")




'''
Example Body:
body = [
    {'text': 'あなたのtーシャツは大好きです。'},    
    {'text': '大学院生です。'} 
]

Example Response:

[{'translations': [{'text': 'I love your t-shirts.', 'to': 'en'}]}, {'translations': [{'text': "I'm a graduate student.", 'to': 'en'}]}]
[
    {
        "translations": [
            {
                "text": "I love your t-shirts.",
                "to": "en"
            }
        ]
    },
    {
        "translations": [
            {
                "text": "I'm a graduate student.",
                "to": "en"
            }
        ]
    }
]

Example Response 2, using auto-detect language:
[
    {
        "detectedLanguage": {
            "language": "ja",
            "score": 1.0
        },
        "translations": [
            {
                "text": "I love your t-shirts.",
                "to": "en"
            }
        ]
    },
    {
        "detectedLanguage": {
            "language": "ja",
            "score": 1.0
        },
        "translations": [
            {
                "text": "I'm a graduate student.",
                "to": "en"
            }
        ]
    }
]
'''

'''
Mock_translation
[
    {
        "detectedLanguage": {
            "language": "es",
            "score": 1.0
        },
        "translations": [
            {
                "text": "Whatever happens, I'm not going to call you",
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
                "text": "Without you I don't do well, I don't do badly either (yes)",
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
'''