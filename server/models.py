
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

db = SQLAlchemy()
# bcrypt = Bcrypt()


class User ( db.Model ) :

    __tablename__ = "users"

    id = db.Column ( db.Integer, primary_key = True )
    username = db.Column ( db.String ( 255 ), unique = True, nullable = False )
    email = db.Column ( db.String ( 255 ), unique = True, nullable = False )
    password_hash = db.Column ( db.String ( 255 ), nullable = False )
    # Roles so far : Admin, Manager
    role = db.Column ( db.Enum ( "admin", "manager", name = "user_roles" ), nullable = False, default = "manager" )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )
    # updated_at = db.Column ( db.DateTime, default = datetime.utcnow, onupdate = # CHECK ON HOW TO IMPLEMENT THIS FIELD


    def __repr__ ( self ) :
        return f"<User { self.username }>"
    
    def set_password ( self, password ) :
        self.password_hash = generate_password_hash ( password ).decode ( "utf-8" )
    
    def check_password ( self, password ) :
        return check_password_hash ( self.password_hash, password )