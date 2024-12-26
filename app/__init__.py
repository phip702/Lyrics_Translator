import logging
from flask import Flask
from .extensions import db, migrate
from .routes.main import main
from .routes.playlist import playlist
from .routes.track import track
#delete from .models import Track, Lyrics
from dotenv import load_dotenv
from sqlalchemy import inspect
from celery import Celery
from threading import Thread
from app.services.rabbitmq.insert_row_producer import start_producer
from app.services.rabbitmq.insert_row_consumer import start_consumer


def run_rabbitmq_services():
    producer_thread = Thread(target=start_producer)
    consumer_thread = Thread(target=start_consumer)
    producer_thread.start()
    consumer_thread.start()



def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def create_app():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger('pika').setLevel(logging.WARNING)

    load_dotenv()

    app = Flask(__name__)
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config
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

    run_rabbitmq_services()

    #celery = make_celery(app) 
    print("APP INITIALIZED")
    return app#, celery


#C-TODO: message queue
#TODO: implement async via threading for producing and consuming
#TODO: testing
#TODO: analytics --just use my old artifact, don't do anything more
#TODO: push to Heroku
#TODO: continuous integration?
#TODO: continuous delivery?
#TODO: production monitoring instrumenting
#TODO: front end
#TODO: make genius api call ignore 'romanized' versions