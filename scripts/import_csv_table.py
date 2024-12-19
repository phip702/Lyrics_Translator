import csv
from ..extensions import db
from models.track import Track
from __init__ import create_app

# Initialize the Flask app
app = create_app()

# Path to the CSV file
csv_file_path = './test_data/tracks_table.csv'

# Function to import data from the CSV
def import_csv():
    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Loop through each row in the CSV and insert it into the database
        for row in csv_reader:
            # Create a new Track instance
            track = Track(
                spotify_track_id=row['spotify_track_id'],  # Replace with the actual column name
                track_name=row['track_name'],
                track_artist=row['track_artist'],
                track_image=row.get('track_image', ''),  # Optional field, use .get() to avoid errors
                track_date_added=row['track_date_added']  # Ensure this is in the correct format
            )

            # Add the track to the session and commit
            db.session.add(track)
        
        # Commit all changes to the database
        db.session.commit()
        print("Data imported successfully!")

# Run the import function
with app.app_context():  # Use the app context to work with the database
    db.create_all()
    import_csv()
    print(f"Records in session: {db.session.new}")
