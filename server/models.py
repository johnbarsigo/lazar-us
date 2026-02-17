
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
    # Roles created so far : Admin, Manager
    role = db.Column ( db.Enum ( "admin", "manager", name = "user_roles" ), nullable = False, default = "manager" )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )
    updated_at = db.Column ( db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow )



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
    default_rent = db.Column ( db.Numeric(10, 2), nullable = False )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )
    status = db.Column ( db.Enum ( "available", "occupied", name = "room_status" ), nullable = False, default = "available" )

    def __repr__ ( self ) :
        return f"<Room { self.room_number }>"
    

class Tenant ( db.Model ) :

    __tablename__ = "tenants"

    id = db.Column ( db.Integer, primary_key = True )
    name = db.Column ( db.String ( 255 ), nullable = False )
    email = db.Column ( db.String ( 255 ), unique = True, nullable = False )
    phone = db.Column ( db.String ( 20 ), nullable = True )
    national_id = db.Column ( db.String ( 8), unique = True, nullable = False )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )
    updated_at = db.Column ( db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow )

    def __repr__ ( self ) :
        return f"<Tenant { self.id } - { self.name }>"
    

class Occupancy ( db.Model ) :

    __tablename__ = "occupancies"

    id = db.Column ( db.Integer, primary_key = True )
    tenant_id = db.Column ( db.Integer, db.ForeignKey ( "tenants.id" ), nullable = False )
    room_id = db.Column ( db.Integer, db.ForeignKey ( "rooms.id" ), nullable = False )
    agreed_rent = db.Column ( db.Numeric(10, 2), nullable = False )
    start_date = db.Column ( db.Date, nullable = False )
    end_date = db.Column ( db.Date, nullable = True )
    check_in_notes = db.Column ( db.Text, nullable = True )
    check_out_notes = db.Column ( db.Text, nullable = True )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )

    # Relationships
    tenant = db.relationship ( "Tenant", backref = "occupancies" )
    room = db.relationship ( "Room", backref = "occupancies" )

    def __repr__ ( self ) :
        return f"<Occupancy { self.id } - Tenant { self.tenant_id } in Room { self.room_id } started on { self.start_date }>"


class MonthlyCharge ( db.Model ) :

    __tablename__ = "monthly_charges"

    id = db.Column ( db.Integer, primary_key = True )
    occupancy_id = db.Column ( db.Integer, db.ForeignKey ( "occupancies.id" ), nullable = False )
    rent_amount = db.Column ( db.Numeric(10, 2), nullable = False )
    water_bill = db.Column ( db.Numeric(10, 2), nullable = False )
    month = db.Column ( db.String ( 20), nullable = False )
    year = db.Column ( db.Integer, nullable = False )
    charge_date = db.Column ( db.Date, nullable = False )
    other_charges = db.Column ( db.Numeric(10, 2), nullable = True, default = 0.0 )
    created_at = db.Column ( db.DateTime, default = datetime.utcnow )

    # Constraint to counter duplicate billing for the same month and year
    __table_args__ = ( db.UniqueConstraint( "occupancy_id", "month", "year", name= "unique_monthly_charge" ) )

    # Relationships
    occupancy = db.relationship ( "Occupancy", backref = "monthly_charges" )

    def __repr__ ( self ) :
        return f"<MonthlyCharge { self.id } - Occupancy { self.occupancy_id } charged rent { self.rent_amount }, water bill { self.water_bill }, other charges { self.other_charges } on { self.charge_date }>"
    


class Payment ( db.Model ) :

    __tablename__ = "payments"

    id = db.Column ( db.Integer , primary_key = True )

    tenant_id = db.Column ( db.Integer, db.ForeignKey ( "tenants.id" ), nullable = False )
    monthly_charge_id = db.Column ( db.Integer, db.ForeignKey( "monthly_charges.id" ), nullable = False )

    amount = db.Column ( db.Numeric( 10, 2 ), nullable = False )
    method = db.Column ( db.Enum( "mpesa", "cash", "bank", name="payment_methods" ) )
    mpesa_receipt = db.Column ( db.String (100), nullable=True )

    payment_date = db.Column ( db.Date, nullable=False )
    created_at = db.Column ( db.DateTime, default = db.func.current_timestamp() )

    # Relationships
    monthly_charge = db.relationship ( "MonthlyCharge", backref = "payments" )

    def __repr__ ( self ) :
        return f"Payment {self.id} for monthly charge ID :{self.monthly_charge_id}, through {self.method} on {self.payment_date}"