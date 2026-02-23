
from flask import request
from flask_restful import Resource
from auth.jwt import decode_token
from auth.permissions import admin_required, manager_required
from models import db, Tenant, Occupancy, Room
from datetime import datetime


class TenantsList ( Resource ) :

    # Retrieve all tenants and details.
    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self ) :

        tenants = Tenant.query.all()

        return [ {
            "id" : t.id,
            "name" : t.name,
            "email" : t.email,
            "phone number" : t.phone,
            "national_id" : t.national_id,
            "created_at" : t.created_at
        } for t in tenants ], 200


# Work on how to create occupancy after creating tenant. Maybe create occupancy in the same request as tenant creation.
class CreateTenantOccupancy ( Resource ) :

    # Endpoint : POST /api/tenants/check-in
    # Creates tenant with occupancy in one request.

    # Admin/ Manager required.
    @token_required
    @manager_required
    def post ( self ) :

        try :

            data = request.get_json ()

            # Validate required fields for tenant and occupancy creation.
            required_fields = [ "name", "email", "phone", "national_id", "room_id", "agreed_rent", "start_date" ]

            for field in required_fields :
                if field not in data :
                    return { "error" : f"{ field } is required." }, 400
            
            # Verify room availability
            room = Room.query.get ( data [ "room_id" ] )
            if not room or room.status != "available" :
                return { "error" : "Room not available."}, 409

            # Create tenant instance.
            tenant = Tenant (
                name = data [ "name" ],
                email = data [ "email" ],
                phone = data [ "phone" ],
                national_id = data [ "national_id" ]
            )

            db.session.add ( tenant )
            # Getting tenant ID before commit to use it for occupancy creation.
            db.session.flush ()

            # Create occupancy instance linked to the above tenant.
            start_date = datetime.fromisoformat ( data [ "start_date" ] ).date()
            occupancy = Occupancy (
                tenant_id = tenant.id,
                room_id = data [ "room_id" ],
                agreed_rent = data [ "agreed_rent" ],
                start_date = start_date
            )

            db.session.add ( occupancy )
            db.session.commit ()

            # Update room status to occupied.
            room.status = "occupied"
            db.session.commit ()

            return {
                "message" : f"Tenant id { tenant.id }, { tenant.name } created successfully and checked into room { room.room_number }. Check-in date: { start_date }."
            }, 201
        
        except Exception as e :
            return { "error" : str (e) }, 500


class TenantDetails ( Resource ) :

    # Retireve specific tenant and details.
    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        # To retrieve the tenant's occupancy details as well.
        occupancies = tenant.occupancies
        
        return {
            "id" : tenant.id,
            "name" : tenant.name,
            "email" : tenant.email,
            "phone number" : tenant.phone,
            "national_id" : tenant.national_id,
            "room_id" : occupancies [ -1 ].room_id if occupancies else None, # Get the room_id of the most recent occupancy if it exists, otherwise return None. Occupancies are ordered by start_date, so the most recent occupancy will be the last one in the list. [-1] takes the last element of the list.
            "created_at" : tenant.created_at
        }, 200

    # Update tenant details (name, email, phone, national_id). Work on how to update occupancy details if tenant details are updated. Maybe create a separate endpoint for updating occupancy details.

    # Admin/ Manager required.
    @token_required
    @manager_required
    def put ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        data = request.get_json ()

        tenant.name = data.get ( "name", tenant.name )
        tenant.email = data.get ( "email", tenant.email )
        tenant.phone = data.get ( "phone", tenant.phone )
        tenant.national_id = data.get ( "national_id", tenant.national_id )

        db.session.commit ()

        return { "message" : f"Tenant id { tenant.id }, { tenant.name } updated successfully." }, 200
    
    # Delete tenant. Work on how to handle occupancy and billing details when a tenant is deleted. Maybe set occupancy end date to current date and mark all future billings as cancelled or delete them.
    # Theory : Delete tenant, set occupancy end date to current date, delete all future billings. This way we maintain historical data for past occupancies and billings while ensuring that no future charges are generated for the deleted tenant.

    # Admin required.
    @token_required
    @admin_required
    def delete ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        db.session.delete ( tenant )
        db.session.commit ()

        return { "message" : "Tenant deleted successfully." }, 200



# Retrieves a tenant's list of occupancies. This will allow us to show the tenant's current and past occupancies when we retrieve their details.
class TenantOccupancies ( Resource ) :

    # Admin required.
    @token_required
    @admin_required
    def get ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        occupancies = tenant.occupancies

        return [ {
            "id" : o.id,
            "room_id" : o.room_id,
            "agreed_rent" : o.agreed_rent,
            "start_date" : o.start_date,
            "end_date" : o.end_date
        } for o in occupancies ], 200
    


# Retrieve a tenant's active occupancy, all monthly charges, all payments and running balances. 
class TenantLedger ( Resource ) :

    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        occupancies = tenant.occupancies

        ledger = []

        for o in occupancies :
            charges = o.monthly_charges
            payments = [ p for c in charges for p in c.payments ] # Flatten the list of payments from all charges.

            for c in charges :
                ledger.append ( {
                    "type" : "charge",
                    "amount" : c.rent_amount + c.water_bill,
                    "date" : c.charge_date
                } )
            
            for p in payments :
                ledger.append ( {
                    "type" : "payment",
                    "amount" : p.amount,
                    "date" : p.payment_date
                } )
        
        # Sort the ledger by date.
        ledger.sort ( key = lambda x : x [ "date" ] )

        return ledger, 200