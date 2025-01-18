import logging
from flask import Flask
from .extensions import db, migrate
from .routes.main import main
from .routes.playlist import playlist
from .routes.track import track
from .routes.analytics import analytics
#delete from .models import Track, Lyrics
from dotenv import load_dotenv
import os
from sqlalchemy import inspect
from threading import Thread
from app.services.rabbitmq.insert_row_producer import start_producer
from app.services.rabbitmq.insert_row_consumer import start_consumer
from metrics import metrics

def run_rabbitmq_services():
    producer_thread = Thread(target=start_producer)
    consumer_thread = Thread(target=start_consumer)
    producer_thread.start()
    consumer_thread.start()


def create_app(): 
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger('pika').setLevel(logging.WARNING) #* SET LOG LEVEL

    load_dotenv()
    print(f"FLASK ENV: {os.getenv('FLASK_ENV')}")

    app = Flask(__name__, static_url_path="", static_folder="static")
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    print("Current directory:", os.getcwd())
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/db.sqlite3'

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['RABBITMQ_URL'] = os.getenv('RABBITMQ_URL')
    db.init_app(app)
    migrate.init_app(app,db)

    metrics.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(playlist)
    app.register_blueprint(track)
    app.register_blueprint(analytics)
    
    with app.app_context():
        db.create_all()  # Initializes tables that do not already exist
        inspector = inspect(db.engine)  # Create an inspector object to inspect the database engine
        tables = inspector.get_table_names()  # Get the list of table names
        logging.critical("Tables Initialized: %s", tables)

    run_rabbitmq_services()

    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    # Log the database path
    print(f"Inserting into database located at: {db_path}")

    print("APP INITIALIZED")
    return app


#C-TODO: message queue
#C-TODO: implement async via threading for producing and consuming
#C-TODO: playlist click track -> track page
#C-TODO: integration testing
#C-TODO: unit testing
#C-TODO: analytics --just use my old artifact, don't do anything more
#C-TODO: front end (HTML template/polymorphism, CSS)
#C-TODO: Add buffering/loading indication
#C-TODO: live deploy
#TODO: production monitoring instrumenting
#TODO: continuous integration?
#TODO: continuous delivery?

#TODO: make genius api call ignore 'romanized' versions; enforce language selection by user
#C-TODO: make playlist become side menu after user selects track