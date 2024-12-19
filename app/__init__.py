from flask import Flask

from .extensions import db, migrate
from .routes.main import main
from .routes.lyrics import lyrics
from .routes.track import track
#from .models import * 
from .models.track import Track #removing this fixed a blueprint not registered error for scripts/import_csv_table
from dotenv import load_dotenv
from sqlalchemy import inspect



def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.secret_key = 'sjfa90u3214sfdfaJIS0324'  # Necessary for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(main)
    app.register_blueprint(lyrics)
    app.register_blueprint(track)

    
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        print("Tables:", inspector.get_table_names())
        first_row = Track.query.first()
        print(first_row)
        
        
    print("APP INITIALIZED")
    return app