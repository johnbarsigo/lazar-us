
from flask import request, g, jsonify
from auth.jwt import decode_token
from functools import wraps
from models import User


# def get_current_user () :

#     bearer = request.headers.get ( "Authorization" )

#     if not bearer or not bearer.startswith ( "Bearer " ) :
#         return None
    
#     token = bearer.split ( " " ) [ 1 ]

#     user_id, error = decode_token ( token )

#     if error :
#         return None
    
#     return token, User.query.get ( user_id )


# def admin_required ( f ) :

#     def wrapper ( *args, **kwargs ) :

#         user = get_current_user ()

#         if not user :
#             return { "error" : "Unauthorized" }, 401
        
#         token, user_obj = user

#         if user_obj.role != "admin" :
#             return { "error" : "Forbidden" }, 403
        
#         return f ( *args, **kwargs )
    
#     wrapper.__name__ = f.__name__

#     return wrapper


def admin_required ( f ) :

    @wraps ( f )
    def decorated ( *args, **kwargs ) :

        if not hasattr ( g, "current_user" ) :
            return { "error" : "Authentication required." }, 403
        
        if g.current_user.role != "admin" :
            return { "error" : "Admin access required." }, 403
        
        return f ( *args, **kwargs )

    return decorated


def manager_required ( f ) :

    @wraps ( f )
    def decorated ( *args, **kwargs ) :
        
        if not hasattr ( g, "current_user" ) :
            return { "error" : "Authentication required." }, 401
        
        if g.current_user.role not in [ "admin", "manager" ] :
            return { "error" : "Manager access required." }, 403
        
        return f ( *args, **kwargs )

    return decorated


# def manager_required ( f ) :

#     def wrapper ( *args, **kwargs ) :

#         user = get_current_user ()

#         if not user :
#             return { "error" : "Unauthorized" }, 401
        
#         token, user_obj = user

#         if user_obj.role not in [ "admin", "manager" ] :
#             return { "error" : "Forbidden" }, 403
        
#         return f ( *args, **kwargs )
    
#     wrapper.__name__ = f.__name__

#     return wrapper


