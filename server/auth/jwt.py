
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, jwt_required as jwt_required_decorator
from datetime import datetime, timedelta
from flask import current_app, g, jsonify
from functools import wraps
from models import User

DEFAULT_EXPIRATION_DELTA = timedelta ( hours = 1 )

def token_required ( f ) :

    # Combined decorator that verifies JWT token (@jwt_required) and loads the user from the database (@token_required). This allows us to access the current user in downstream decorators like @admin_required without needing to decode the token multiple times.

    @jwt_required_decorator () # Verify JWT token.
    @wraps ( f )
    def decorated ( *args, **kwargs ) :

        try :
            token_data = get_jwt ()
            user_id = token_data.get ( "sub" )

            if not user_id :
                return { "error" : "Invalid token structure." }, 401
            
            # Lookup user in database.
            user = User.query.get ( user_id )
            if not user :
                return { "error" : "User not found." }, 404
            
            # Store both ID and user object for downstream decorators
            g.current_user_id = user_id
            g.current_user = user
        
        except Exception as e :
            return { "error" : f"Authentication failed: { str(e) }"}
        
        return f ( *args, **kwargs )
    
    return decorated


# def generate_token ( user_id, role, expiration_delta = DEFAULT_EXPIRATION_DELTA, secret_key = DEFAULT_SECRET_KEY ) :

#     payload = {
#         "id" : user_id,
#         "role" : role,
#         "exp" : datetime.utcnow ( ) + expiration_delta
#     }

#     token = jwt.encode (
#         payload,
#         secret_key,
#         algorithm = "HS256"
#     )

#     return token


# Generate JWT access token
def generate_token ( user_id, user_role ) :

    # Create JWT token with user role in claims.
    additional_claims = { "role" : user_role }
    token = create_access_token (
        identity = user_id,
        additional_claims = additional_claims,
        expires_delta = DEFAULT_EXPIRATION_DELTA
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