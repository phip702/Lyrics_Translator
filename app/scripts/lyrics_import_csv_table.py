import logging
import csv
from ..extensions import db
from ..models.lyrics import Lyrics
from .. import create_app
from sqlalchemy import inspect
from datetime import datetime

# Initialize the Flask app
app = create_app()

# Path to the CSV file
csv_file_path = 'app/test_data/lyrics_table.csv'

# Function to import data from the CSV
def import_lyrics_csv():
    successful_rows = 0
    
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Loop through each row in the CSV and insert it into the database
        for row in csv_reader:
            try:
                # Convert track_date_added string to a datetime object
                lyrics_date_added = datetime.fromisoformat(row['lyrics_date_added'])
                lyrics = Lyrics(
                    spotify_track_id=row['spotify_track_id'],  
                    original_lyrics=row['original_lyrics'],
                    translated_lyrics=row['translated_lyrics'],
                    detected_language=row['detected_language'],  
                    lyrics_date_added=lyrics_date_added
                )
                
                db.session.add(lyrics)
                successful_rows += 1

            except Exception as e:
                print(f"Error processing row: {row['spotify_track_id']}. Error: {e}")

        try:
            # Commit all changes to the database
            db.session.commit()
            logging.debug(f"Lyrics imported successfully! Rows committed: {successful_rows}")
        except Exception as e:
            logging.debug(f"Error during commit: {e}")
            db.session.rollback()

# Run the import function
with app.app_context():  # Use the app context to work with the database
    db.create_all()
    inspector = inspect(db.engine)
    logging.debug("Tables: %s", inspector.get_table_names())
    import_lyrics_csv()
    logging.debug(f"Records in session: {db.session.new}")
