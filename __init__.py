from flask import Flask

from .extensions import db, migrate
from .routes.main import main
from .routes.lyrics import lyrics
from .routes.track import track
from dotenv import load_dotenv

def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app,db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(lyrics)
    app.register_blueprint(track)

    return app
