#!/usr/bin/env python3
from flask import Flask
import os
from dotenv import load_dotenv
import logging

from .extensions import db
from .views import main
from .utils import make_celery

import sys
sys.path.append('../')

def create_app():
    # Load environment variables
    load_dotenv()

    # Determine base directory and template location
    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    template_folder = os.path.join(parent_directory, 'templates')

    # Create the Flask app with specific template folder
    app = Flask(__name__, template_folder=template_folder)

    # Configure app
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    app.config['CELERY_CONFIG'] = {"broker_url": 'amqps://csgaqrgu:kF83BEpmQIdLMXkSTYq6Y03VCiwDRAxj@moose.rmq.cloudamqp.com/csgaqrgu',
                                "result_backend": 'amqps://csgaqrgu:kF83BEpmQIdLMXkSTYq6Y03VCiwDRAxj@moose.rmq.cloudamqp.com/csgaqrgu'}

    # Set up logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Database configuration
    uri = os.getenv("DATABASE_URL")
    logging.debug(f"uri: {uri}")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    logging.debug(f"uri: {uri}")
    db.init_app(app)
    
    celery = make_celery(app)
    celery.set_default() #not sure if necessary

    app.register_blueprint(main)

    return app ,celery  #this makes the app unable to find application or factory in module 'app'