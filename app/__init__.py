import logging
from flask import Flask
from .extensions import db, migrate
from .routes.main import main
from .routes.playlist import playlist
from .routes.track import track
from .models import Track, Lyrics
from dotenv import load_dotenv
from sqlalchemy import inspect



def create_app():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    load_dotenv()

    app = Flask(__name__)
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #app.app_context().push()

    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(main)
    app.register_blueprint(playlist)
    app.register_blueprint(track)

    
    with app.app_context():
        db.create_all()  # Initializes tables that do not already exist
        inspector = inspect(db.engine)  # Create an inspector object to inspect the database engine
        tables = inspector.get_table_names()  # Get the list of table names
        logging.critical("Tables Initialized: %s", tables)
        
        
    print("APP INITIALIZED")
    return app