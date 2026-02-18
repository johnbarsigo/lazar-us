
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from flask import request, jsonify

jwt = JWTManager ()



def login_user ( username, user_id ) :

    access_token = create_access_token ( identity = user_id )

    return { "access_token" : access_token, "username" : username }



def token_required ( f ) :

    @wraps ( f )
    
    def decorated ( *args, **kwargs ) :

        token = None

        if "Authorization" in request.headers :

            token = request.headers [ "Authorization" ].split()[1]
        
        if not token :

            return { "error" : "Token missing." }, 401
        
        try :

            from flask_jwt_extended import decode_token
            decoded = decode_token ( token )
            request.user_id = decoded [ "sub" ]
        
        except :
            return { "error" : "Invalid token." }, 401
        
        return f ( *args, **kwargs )
    
    return decorated