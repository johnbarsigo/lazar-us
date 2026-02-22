
from flask import request, jsonify
from models import db, User
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash # Remove password hashing from models.py and use werkzeug here for better integration with Flask
from auth.jwt import decode_token
from auth.permissions import admin_required, manager_required

# NOTE : password_hash is the column name in the User model.


# List all users in the system. Admin required.
class UsersList ( Resource ) :

    # Admin required.
    @token_required
    @admin_required
    def get ( self ) :
        
        users = User.query.all ()

        return jsonify ( [ {
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
            "role" : user.role,
            "created_at" : user.created_at.isoformat(),
            "updated_at" : user.updated_at.isoformat()
        } for user in users ] )



class CreateUser ( Resource ) :

    # Create new user
    # Admin required
    @token_required
    @admin_required
    def post ( self ) :

        try :

            data = request.get_json ()

            # Validate input
            if not data.get( "username" ) or not data.get ( "email" ) or not data.get ( "password" ) or not data.get ( "role" ):
                return { "error" : "Username, email, password and role are required." }, 400

            # Check if the username or email already exists
            if User.query.filter_by ( username = data [ "username" ] ).first () :
                return { "error" : "Username already exists." }, 400
            
            # Check if the email already exists
            if User.query.filter_by ( email = data [ "email" ] ).first () :
                return { "error" : "Email already exists." }, 400
            
            # Collecting new user data.
            user = User (
                username = data [ "username" ],
                email = data [ "email" ],
                # Hashing the password before storing
                password_hash = generate_password_hash ( data [ "password" ] ),
                role = data.get ( "role", "manager" ) # Defaults to manager
            )

            db.session.add ( user )
            db.session.commit ()
        
        except Exception as e :
            db.session.rollback ()
            return { "error" : str(e) }, 500

        return { "message" : f"User ID: {user.id}, name {user.name} registered successfully." }



class UserLogin ( Resource ) :
    
    # Login user
    def post ( self ) :

        try :

            data = request.get_json ()

            if not data or not data.get ( "username" ) or not data.get ( "password" ) :
                return { "error" : "Missing credentials."}, 400

            user = User.query.filter_by ( username = data [ "username" ] ).first()

            if not user or not check_password_hash ( user.password_hash, data [ "password" ] ) :
                return { "error" : "Invalid username or password." }, 401
            
            # Generate JWT token
            token = generate_token ( user.id, user.role )

            return { "message" : f"Login successful, welcome {user.name}!" }, 200
        
        except Exception as e :
            return { "error" : str (e) }, 500



class UserDetails ( Resource ) :

    # Show logged in User details.
    @token_required
    def get ( self, user_id ) :

        user = User.query.get ( user_id )

        if not user :
            return { "error" : "User not found." }, 404
        
        return {
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
            "role" : user.role,
            "created_at" : user.created_at.isoformat(),
            "updated_at" : user.updated_at.isoformat()
        }

    # Update user details (username, email, password).
    # Admin required
    @token_required
    @admin_required
    def put ( self, user_id ) :

        user = User.query.get ( user_id )

        if not user :
            return { "error" : "User not found." }, 404
        
        data = request.get_json ()

        if data.get ( "username" ) :
            user.username = data [ "username" ]

            # LATER UPDATE TO CHECK IF THE NEW USERNAME ALREADY EXISTS IN THE DATABASE TO AVOID DUPLICATES.
        
        if data.get ( "email" ) :
            user.email = data [ "email" ]
        
        if data.get ( "password" ) :
            user.password_hash = generate_password_hash ( data [ "password" ] )
        
        # Update the timestamp for when the user details were last updated.
        user.updated_at = db.func.now ()
        
        db.session.commit ()

        return { "message" : "User details updated successfully." }
    

    # Delete user account.
    # Admin required.
    @token_required
    @admin_required
    def delete ( self, user_id ) :

        user = User.query.get ( user_id )

        if not user :
            return { "error" : "User not found." }, 404
        
        db.session.delete ( user )
        db.session.commit ()

        return { "message" : "User account deleted successfully." }
