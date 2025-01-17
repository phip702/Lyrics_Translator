import lyricsgenius
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from ..handlers.lyrics_handler import trim_lyrics
import logging
import json
import unicodedata

def get_genius_auth_token(): #*do not delete, this is called on the home page
    load_dotenv()
    genius_auth_token = os.getenv("GENIUS_AUTH_TOKEN")
    return genius_auth_token


def remove_accents_if_latin(input_str):
    """
    Normalize a string to remove accents only if it contains Latin characters.
    """
    if any('LATIN' in unicodedata.name(char, '') for char in input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str

def search_song_by_artist(track_artist, hits):
    '''This is used to find the top hit on the Genius song list that has the spotify track_artist's name.
    This solves the issue of a 'featuring xyz' ruining the search.
    This also solves issues with translations being returned first because they are more popular.
    '''

    try:
        for idx, hit in enumerate(hits, start = 1):
            artist_names = hit['result']['artist_names'].lower()
            logging.debug(f"Is {track_artist} == Genius artist name: {artist_names}")
            if remove_accents_if_latin(track_artist.lower()) in remove_accents_if_latin(artist_names): #used in because of issues where there's a (featuring XX)
                logging.debug(f"Genius Hit Number Returned: {idx}")
                genius_url = hit['result']['url'] 
                return genius_url
    except:
        logging.error(f"Could not find {track_artist} in {[hit['result']['artist_names'] for hit in hits]}")
        "No matching artist in hits"
        
         
# I wrote this scraper, not the lyricsgenius module creators
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics_containers = html.find_all('div', attrs={'data-lyrics-container': 'true'})
    lyrics = ''
    if lyrics_containers:
        for container in lyrics_containers:
            lyrics += container.get_text(separator='\n') + '\n'
        lyrics = lyrics.replace('[', '\n[') # adds a line break before [chorus] [verse] etc #this line and the line above take <.0001s
        lyrics = trim_lyrics(lyrics)
        return lyrics
    else:
        return "Could not find lyrics" 


def get_song_lyrics(track_name, track_artist):
    genius_auth_token = os.getenv("GENIUS_AUTH_TOKEN")
    genius = lyricsgenius.Genius(genius_auth_token) #optimize; it might be faster to just use the Genius API from the beginning (or scrape) to get the search results based on track_name and track_artist

    try:
        search_results = genius.search_songs(f"{track_name} {track_artist}", per_page=3) #*track artist going after appears to be more accurate
        hits = search_results['hits']
        logging.debug(f"Genius Hits: {json.dumps(hits, indent=4)}")
        first_hit_url = search_song_by_artist(track_artist, hits)
        return scrape_song_lyrics(first_hit_url)
    except Exception as e:
        logging.error(f"Error while fetching lyrics: {e}")
        return "Could not find lyrics" #this error is to catch when genius.search_songs finds nothing



if __name__ == "__main__": #spot test songs
    from src.spotify_api import get_song_id_from_url, get_track_name_artist_image
    spotify_track_id = get_song_id_from_url("https://open.spotify.com/track/6Za3190Sbw39BBC77WSS1C?si=c57f5e2fa1b649e2")
    print(spotify_track_id)
    track_name, track_artist, track_image  = get_track_name_artist_image(spotify_track_id)
    print(track_name, track_artist)

    search_results = get_song_lyrics(track_name, track_artist)
    print(search_results)