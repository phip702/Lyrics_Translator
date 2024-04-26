# import os
# import logging
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv

# db = SQLAlchemy()

# def create_app():
#     # Load environment variables
#     load_dotenv()

#     # Determine base directory and template location
#     parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#     template_folder = os.path.join(parent_directory, 'templates')

#     # Create the Flask app with specific template folder
#     app = Flask(__name__, template_folder=template_folder)

#     # Configure app
#     app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions

#     # Set up logging
#     logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#     # Database configuration
#     uri = os.getenv("DATABASE_URL")
#     if uri and uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)
#     app.config['SQLALCHEMY_DATABASE_URI'] = uri

#     # Initialize SQLAlchemy
#     db.init_app(app)

#     return app
