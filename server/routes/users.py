
from flask import request, jsonify
from models import db, User
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash # Remove password hashing from models.py and use werkzeug here for better integration with Flask

# NOTE : password_hash is the column name in the User model.


class UserSignUp ( Resource ) :

    # Create new user
    def post ( self ) :

        data = request.get_json ()

        # Validate input
        if not data.get( "username" ) or not data.get ( "email" ) or not data.get ( "password" ) :
            return { "error" : "Username, email and password are required." }, 400

        # Check if the username or email already exists
        if User.query.filter_by ( username = data [ "username" ] ).first () :
            return { "error" : "Username already exists." }, 400
        
        # Check if the username or email already exists
        if User.query.filter_by ( email = data [ "email" ] ).first () :
            return { "error" : "Email already exists." }, 400
        
        # Collecting new user data.
        user = User (
            username = data [ "username" ],
            email = data [ "email" ],
            password_hash = generate_password_hash ( data [ "password" ] ) # Hashing the password before storing
        )

        db.session.add ( user )
        db.session.commit ()

        return { "message" : "User registered successfully." }



class UserLogin ( Resource ) :
    
    # Login user
    def post ( self ) :

        data = request.get_json ()

        user = User.query.filter_by ( username = data [ "username" ] ).first ()

        if not user or not check_password_hash ( user.password_hash, data [ "password" ] ) :
            return { "error" : "Invalid username or password." }, 401

        return { "message" : "Login successful." }



class UserDetails ( Resource ) :

    # Show logged in User details.
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
    def delete ( self ) :

        user = User.query.get ( user_id )

        if not user :
            return { "error" : "User not found." }, 404
        
        db.session.delete ( user )
        db.session.commit ()

        return { "message" : "User account deleted successfully." }


api.add_resource ( UserSignUp, "/api/users/signup" )
api.add_resource ( UserLogin, "/api/users/login" )
api.add_resource ( UserDetails, "/api/users/<int:user_id>" )