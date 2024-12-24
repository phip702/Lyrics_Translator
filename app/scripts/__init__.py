# __init__.py
from .track_import_csv_table import import_track_csv
from .lyrics_import_csv_table import import_lyrics_csv

def run_imports():
    # Run the track import
    import_track_csv()
    # Run the lyrics import
    import_lyrics_csv()
