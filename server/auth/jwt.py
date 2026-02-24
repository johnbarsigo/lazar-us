
from flask_jwt_extended import get_jwt, create_access_token, jwt_required as jwt_required_decorator
from datetime import datetime, timedelta
from flask import current_app, g, jsonify
from functools import wraps
from models import User


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



# Generate JWT access token
def generate_token ( user_id, user_role ) :

    # Create JWT token with user role in claims.
    additional_claims = { "role" : user_role }
    token = create_access_token (
        identity = user_id,
        additional_claims = additional_claims
    )

    return token



def verify_token_manually(token):
    """
    Manually verify and decode a token
    
    Use this for:
    - M-Pesa callbacks (external requests)
    - Background jobs
    - Any context where flask-jwt-extended decorators don't work
    
    Args:
        token (str): The JWT token to verify
        
    Returns:
        tuple: (user_id, error_message) or (None, error_message) if invalid
        
    Example:
        user_id, error = verify_token_manually(token)
        if error:
            return {"error": error}, 401
    """
    try:
        payload = jwt_decode_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            return None, "Invalid token structure"
        
        return user_id, None
    
    except Exception as e:
        return None, f"Token verification failed: {str(e)}"