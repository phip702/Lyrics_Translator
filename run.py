#!/usr/bin/env python3
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001)) # tells Flask to look for the PORT variable assigned by Heroku else use local port 5001
    app.run(host='0.0.0.0', port = port) # 0.0.0.0 means run on all addresses