
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from auth import jwt
from models import db

from routes.users import UserSignUp, UserLogin, UserDetails
from routes.rooms import RoomsList, RoomDetails
from routes.tenants import CreateTenant, TenantsList, TenantDetails, TenantLedger, TenantOccupancies
from routes.billings import GenerateBill, BillingsList, BillingDetails
from routes.payments import PaymentsList, RecordPayment, PaymentDetails
from routes.reports import GenerateArrearsReport
# from routes.occupancies import


def create_app ( ) :

    load_dotenv () # Load environment variables from .env file if it exists

    app = Flask ( __name__ )

    # Load configuration from environment variables

    app.config [ "SQLALCHEMY_DATABASE_URI" ] = os.getenv ( "DATABASE_URL", "sqlite:///oks.db" )
    app.config [ "SQLALCHEMY_TRACK_MODIFICATIONS" ] = False
    app.config [ "JWT_SECRET_KEY" ] = os.getenv ( "JWT_SECRET_KEY", "e7ba32d2feaa467398beb846112494c5" )

    # Initialize extensions

    CORS (
        app,
        supports_credentials = True,
        origins = [ "http://localhost:3000" ],
        allow_headers = [ "Content-Type", "Authorization" ]
    )
    db.init_app ( app )
    # Initiate JWT extension with Flask app
    jwt.init_app ( app )
    Migrate ( app, db )

    api = Api ( app )

    # Register API resources
    api.add_resource ( UserSignUp, "/api/users/signup" )
    api.add_resource ( UserLogin, "/api/users/login" )
    api.add_resource ( UserDetails, "/api/users/<int:user_id>" )

    api.add_resource ( RoomsList, "/api/rooms" )
    api.add_resource ( RoomDetails, "/api/rooms/<int:room_id>" )

    api.add_resource ( CreateTenant, "/api/tenants/create" )
    api.add_resource ( TenantsList, "/api/tenants" )
    api.add_resource ( TenantDetails, "/api/tenants/<int:tenant_id>")
    api.add_resource ( TenantLedger, "/api/tenants/<int:tenant_id>/ledger" )
    api.add_resource ( TenantOccupancies, "/api/tenants/<int:tenant_id>/occupancies" )

    api.add_resource ( GenerateBill, "/api/billings/generate" )
    api.add_resource ( BillingsList, "/api/billings" )
    api.add_resource ( BillingDetails, "/api/billings/<int:billing_id>" ) # NOT YET CREATED

    api.add_resource ( PaymentsList, "/api/payments" )
    api.add_resource ( RecordPayment, "/api/payments/record" )
    api.add_resource ( PaymentDetails, "/api/payments/<int:payment_id>" )

    api.add_resource ( GenerateArrearsReport, "/api/reports/arrears" )
    # api.add_resource ( " To be filled. " )

    return app


app = create_app ()

if __name__ == "__main__" :
    app.run ( debug = True, port = 5555 )