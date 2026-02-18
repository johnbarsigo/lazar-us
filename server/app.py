
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db


def create_app ( ) :

    app = Flask ( __name__ )

    # Load configuration from environment variables

    app.config [ "SQLALCHEMY_DATABASE_URI" ] = os.getenv ( "DATABASE_URL", "sqlite:///oks.db" )
    app.config [ "SQLALCHEMY_TRACK_MODIFICATIONS" ] = False
    app.config [ "SECRET_KEY" ] = "my-voice-is-my-password"

    # Initialize extensions

    CORS (
        app,
        supports_credentials = True,
        origins = [ "http://localhost:3000" ],
        allow_headers = [ "Content-Type", "Authorization" ]
    )
    db.init_app ( app )
    Migrate ( app, db )

    api = Api ( app )

    return app


app = create_app ()

if __name__ == "__main__" :
    app.run ( debug = True, port = 5555 )