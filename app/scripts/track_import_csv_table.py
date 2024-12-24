import logging
import csv
from ..extensions import db
from ..models.track import Track
from .. import create_app
from sqlalchemy import inspect
from datetime import datetime

# Initialize the Flask app
app = create_app()

# Path to the CSV file
csv_file_path = 'app/test_data/tracks_table.csv'

# Function to import data from the CSV
def import_track_csv():
    successful_rows = 0

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Loop through each row in the CSV and insert it into the database
        for row in csv_reader:
            try:
                # Convert track_date_added string to a datetime object
                track_date_added_formatted = datetime.fromisoformat(row['track_date_added'])

                # Create a new Track instance
                track = Track(
                    spotify_track_id=row['spotify_track_id'],  # Replace with the actual column name
                    track_name=row['track_name'],
                    track_artist=row['track_artist'],
                    track_image=row.get('track_image', ''),  # Optional field, use .get() to avoid errors
                    track_date_added=track_date_added_formatted  # Ensure this is in the correct format
                )

                db.session.add(track)
                successful_rows += 1

            except Exception as e:
                print(f"Error processing row: {row['spotify_track_id']} | {row['track_name']}. Error: {e}")

        try:
            # Commit all changes to the database
            db.session.commit()
            logging.debug(f"Tracks imported successfully! Rows committed: {successful_rows}")
        except Exception as e:
            logging.debug(f"Error during commit: {e}")
            db.session.rollback()

# Run the import function
with app.app_context():  # Use the app context to work with the database
    db.create_all()
    inspector = inspect(db.engine)
    logging.debug("Tables: %s", inspector.get_table_names())
    import_track_csv()
    logging.debug(f"Records in session: {db.session.new}")
