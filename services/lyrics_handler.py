from .azure_translate import create_translation_map, get_translation_for_original
import logging

def trim_lyrics(lyrics):
    ''' Removes the empty lines before and after the lyrics. '''
    lines = lyrics.split('\n')
    start_index = next((i for i, line in enumerate(lines) if line.strip()), 0)
    end_index = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip()), len(lines))
    return '\n'.join(lines[start_index:end_index + 1])

def create_lyrics_set(lyrics): #lyrics should be retrieved from get_song_lyrics (genius_api.py)
    lines = lyrics.splitlines()
    lyrics_set = set(lines)
    logging.debug("Translation Lines Compression: %d vs %d", len(lines), len(lyrics_set))
    return lyrics_set

def get_translated_lyrics(lyrics):
    '''
    This takes a str(lyrics) that should be called from get_song_lyrics (from the genius_api.py) and makes a set of the lyrics to make less calls to the API. 
    It will then call the API, get the translated text for the lyrics_set, and then map it to the original lyrics to populate then return the translated_lyrics.

    Returns: translated lyrics and detected language
    '''
    lines = lyrics.splitlines()
    lyrics_set = create_lyrics_set(lyrics)
    translation_map, detected_language = create_translation_map(lyrics_set)

    translated_lyrics = ''
    for line in lines:
         translated_lyrics += get_translation_for_original(translation_map, line)+'\n'

    translated_lyrics = trim_lyrics(translated_lyrics)
    return translated_lyrics, detected_language