
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



    def __repr__ ( self ) :
        return f"<User { self.username }>"
    
    def set_password ( self, password ) :
        self.password_hash = generate_password_hash ( password ).decode ( "utf-8" )
    
    def check_password ( self, password ) :
        return check_password_hash ( self.password_hash, password )


class Room ( db.Model ) :

    __tablename__ = "rooms"

    id = db.Column ( db.Integer, primary_key = True )
    room_number = db.Column ( db.String ( 3 ), unique = True, nullable = False )
    capacity = db.Column ( db.Integer, nullable = False, default = 1 )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )
    status = db.Column ( db.Enum ( "available", "occupied", name = "room_status" ), nullable = False, default = "available" )

    def __repr__ ( self ) :
        return f"<Room { self.name }>"
    

class Tenant ( db.Model ) :

    __tablename__ = tenants

    id = db.Column ( db.Integer, primary_key = True )
    name = db.Column ( db.String ( 255 ), nullable = False )
    email = db.Column ( db.String ( 255 ), unique = True, nullable = False )
    phone = db.Column ( db.String ( 20 ), nullable = True )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )