
from flask_jwt_extended import JWTManager, get_jwt, create_access_token
from datetime import datetime, timedelta
from flask import current_app, g, jsonify
from functools import wraps
from models import User

DEFAULT_EXPIRATION_DELTA = timedelta ( hours = 1 )
DEFAULT_SECRET_KEY = "e7ba32d2feaa467398beb846112494c5"


def generate_token ( user_id, role, expiration_delta = DEFAULT_EXPIRATION_DELTA, secret_key = DEFAULT_SECRET_KEY ) :

    payload = {
        "id" : user_id,
        "role" : role,
        "exp" : datetime.utcnow ( ) + expiration_delta
    }

    token = jwt.encode (
        payload,
        secret_key,
        algorithm = "HS256"
    )

    return token


def decode_token ( token, secret_key = DEFAULT_SECRET_KEY ) :

    try :
        payload = jwt.decode (
            token,
            secret_key,
            algorithms = [ "HS256" ]
        )
    
    except jwt.ExpiredSignatureError :
        return None, "Token has expired."
    
    except jwt.InvalidTokenError :
        return None, "Invalid token."
    
    return payload [ "id" ], None