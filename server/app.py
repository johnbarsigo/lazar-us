
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from auth.jwt import generate_token
from models import db, timedelta

from routes.users import UsersList, CreateUser, UserLogin, UserDetails
from routes.rooms import RoomsList, RoomDetails
from routes.tenants import CreateTenantOccupancy, TenantsList, TenantDetails, TenantLedger, TenantOccupancies
from routes.billings import GenerateMonthlyBillings, BillingsList, BillingDetails
from routes.payments import PaymentsList, RecordPayment, PaymentDetails
from routes.reports import GenerateArrearsReport
from routes.occupancies import Occupancies, OccupancyDetails


def create_app ( ) :

    load_dotenv () # Load environment variables from .env file if it exists

    app = Flask ( __name__ )

    # Load configuration from environment variables

    app.config [ "SQLALCHEMY_DATABASE_URI" ] = os.getenv ( "DATABASE_URL", "sqlite:///oks.db" )
    app.config [ "SQLALCHEMY_TRACK_MODIFICATIONS" ] = False
    
    app.config [ "JWT_SECRET_KEY" ] = os.getenv ( "JWT_SECRET_KEY", "e7ba32d2feaa467398beb846112494c5" )
    # Set JWT token expiration time
    app.config [ "JWT_ACCESS_TOKEN_EXPIRES" ] = timedelta ( hours = 1 ) 

    # Initialize extensions

    CORS (
        app,
        supports_credentials = True,
        origins = [ "http://localhost:3000" ],
        allow_headers = [ "Content-Type", "Authorization" ]
    )
    db.init_app ( app )
    # Initiate JWT extension with Flask app
    jwt = JWTManager ( app )
    jwt.init_app( app )
    Migrate ( app, db )

    api = Api ( app )

    # Register API resources
    api.add_resource ( UsersList, "/api/users" )
    api.add_resource ( CreateUser, "/api/users/create" )
    api.add_resource ( UserLogin, "/api/users/login" )
    api.add_resource ( UserDetails, "/api/users/<int:user_id>" )

    api.add_resource ( RoomsList, "/api/rooms" )
    api.add_resource ( RoomDetails, "/api/rooms/<int:room_id>" )

    api.add_resource ( CreateTenantOccupancy, "/api/tenants/check-in" ) # Handles both new tenant-occupancy instances (NEW TENANT) and new occupancies for existing tenants (ROOM SWITCH).
    api.add_resource ( TenantsList, "/api/tenants" )
    api.add_resource ( TenantDetails, "/api/tenants/<int:tenant_id>")
    api.add_resource ( TenantLedger, "/api/tenants/<int:tenant_id>/ledger" )
    api.add_resource ( TenantOccupancies, "/api/tenants/<int:tenant_id>/occupancies" )

    api.add_resource ( Occupancies, "/api/occupancies" )
    api.add_resource ( OccupancyDetails, "/api/occupancies/<int:occupancy_id>" )

    api.add_resource ( GenerateMonthlyBillings, "/api/billings/generate" )
    api.add_resource ( BillingsList, "/api/billings" )
    api.add_resource ( BillingDetails, "/api/billings/<int:billing_id>" )

    api.add_resource ( PaymentsList, "/api/payments" )
    api.add_resource ( RecordPayment, "/api/payments/record" )
    api.add_resource ( PaymentDetails, "/api/payments/<int:payment_id>" )

    api.add_resource ( GenerateArrearsReport, "/api/reports/arrears" )
   

    return app


app = create_app ()

if __name__ == "__main__" :
    app.run ( debug = True, port = 5555 )