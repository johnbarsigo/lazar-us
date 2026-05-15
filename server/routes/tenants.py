
from flask import request
from flask_restful import Resource
# from auth.permissions import admin_required, manager_required
# from auth.jwt import token_required
from auth.permissions import require_admin, require_manager
from models import db, Tenant, Occupancy, Room
from datetime import datetime


class TenantsList ( Resource ) :
    # /api/tenants

    # Retrieve all tenants and details.
    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        tenants = Tenant.query.all()

        # separate all tenants with active occupancies ( where end_date is null ) and those without active occupancies. This way we can show active tenants with their room details at the top and past tenants at the bottom.

        active_tenants = []
        past_tenants = []

        for t in tenants :
            if t.occupancies and any ( o.end_date is None for o in t.occupancies ) :
                active_tenants.append ( t )
            else :
                past_tenants.append ( t )

        # return [ {
        #     "id" : t.id,
        #     "name" : t.name,
        #     "email" : t.email,
        #     "phone number" : t.phone,
        #     "national_id" : t.national_id,
        #     "room_number" : t.occupancies [ -1 ].room.room_number if t.occupancies else None, # Get the room number of the most recent occupancy if it exists, otherwise return None. Occupancies are ordered by start_date, so the most recent occupancy will be the last one in the list. [-1] takes the last element of the list.
        #     "occupancy_start_date" : str (t.occupancies [ -1 ].start_date) if t.occupancies else None,
        #     "created_at" : str (t.created_at)
        # } for t in active_tenants ], 200
        
        return [ {
            "id" : t.id,
            "name" : t.name,
            "email" : t.email,
            "phone number" : t.phone,
            "national_id" : t.national_id,
            "room_number" : t.occupancies [ -1 ].room.room_number if t.occupancies else None, # Get the room number of the most recent occupancy if it exists, otherwise return None. Occupancies are ordered by start_date, so the most recent occupancy will be the last one in the list. [-1] takes the last element of the list.
            "occupancy_start_date" : str (t.occupancies [ -1 ].start_date) if t.occupancies else None,
            "created_at" : str (t.created_at)
        } for t in active_tenants ] + ["--- Past Tenants below ---"] + [ {
            "id" : t.id,
            "name" : t.name,
            "email" : t.email,
            "phone number" : t.phone,
            "national_id" : t.national_id,
            "room_number" : t.occupancies [ -1 ].room.room_number if t.occupancies else None,
            "occupancy_start_date" : str (t.occupancies [ -1 ].start_date) if t.occupancies else None,
            "created_at" : str (t.created_at)
        } for t in past_tenants ], 200



# Create occupancy in the same request as tenant creation.
class CreateTenantOccupancy ( Resource ) :

    # Endpoint : POST /api/tenants/check-in
    # Creates tenant with occupancy in one request.

    # Endpoint : POST /api/tenants/<int:tenant_id>/occupancies
    # Creates a new occupancy for an existing tenant.

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def post ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        try :

            data = request.get_json ()

            # OPTION 1 : NEW TENANT AND OCCUPANCY
            if "name" in data and "email" in data and "tenant_id" not in data :
                return self.create_tenant_and_occupancy ( data )
            
            # OPTION 2 : NEW OCCUPANCY FOR EXISTING TENANT
            elif "tenant_id" in data and "name" not in data and "email" not in data :
                return self.create_new_occupancy_for_existing_tenant ( data )
            
            else :
                return {
                    "error" : "Invalid request.",
                    "message" : "Either provide new tenant name or existing tenant_id. Do not provide both."
                }
        
        except Exception as e :
            db.session.rollback ()
            return { "error" : str (e) }, 500


    def create_tenant_and_occupancy ( self, data ) :

        try :

            data = request.get_json ()

            # Validate required fields for tenant and occupancy creation.
            # required_fields = [ "name", "email", "phone", "national_id", "room_id", "agreed_rent", "start_date" ]
            required_fields = [ "name", "email", "phone", "national_id", "room_id", "agreed_rent" ]

            for field in required_fields :
                if field not in data :
                    return { "error" : f"{ field } is required." }, 400
            
            # Check if tenant with the same national_id already exists.
            if Tenant.query.filter_by ( national_id = data [ "national_id" ] ).first () :
                return { "error" : "Tenant with same national id already exists."}
            
            # Check if tenant with the same email already exists.
            if Tenant.query.filter_by ( email = data [ "email" ] ).first () :
                return { "error" : "Tenant with same email already exists."}
            
            # Verify room availability
            room = Room.query.get ( data [ "room_id" ] )
            # if not room or room.status != "available" :
            #     return { "error" : "Room not available."}, 409

            if not room :
                return { "error" : "Not an existing room" }, 409

            if room.status != "available" :
                return { "error" : "Room has been booked." }, 409

            # try :
            #     start_date = datetime.fromisoformat ( data [ "start_date" ] ).date()
            # except :
            #     return { "error" : "Invalid date format for start_date. Use ISO format (YYYY-MM-DD)." }, 400

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
            occupancy = Occupancy (
                tenant_id = tenant.id,
                room_id = data [ "room_id" ],
                agreed_rent = data [ "agreed_rent" ],
                start_date = datetime.utcnow().date(),
                created_at = datetime.utcnow()
            )

            db.session.add ( occupancy )
            db.session.commit ()

            # Update room status to occupied.
            room.status = "occupied"
            db.session.commit ()

            return {
                "message" : f"Tenant id { tenant.id }, { tenant.name } created successfully and checked into room { room.room_number }. Check-in date: { str (occupancy.start_date) }."
            }, 201
        
        except Exception as e :
            return { "error" : str (e) }, 500
    
    def create_new_occupancy_for_existing_tenant ( self, data ) :

        # try:
            
        #     with db.session.begin():
                
        #         active_occupancy = Occupancy.query.filter_by(
        #             tenant_id=data["tenant_id"],
        #             end_date=None   
        #         ).first()
                
        #         new_room = (
        #             db.session.query(Room)
        #             .filter(Room.id == data["room_id"])
        #             # .with_for_update()
        #             .first()
        #         )
                
        #         switch_date = datetime.utcnow().date()
                
        #         active_occupancy.end_date = switch_date
                
        #         old_room = Room.query.get(active_occupancy.room_id)
        #         old_room.status = "available"
        #         old_room.current_occupant_id = None
                
        #         new_occupancy = Occupancy(
        #             tenant_id=data["tenant_id"],
        #             room_id=data["room_id"],
        #             agreed_rent=data["agreed_rent"],
        #             start_date=switch_date
        #         )
                
        #         db.session.add(new_occupancy)
                
        #         new_room.status = "occupied"
        #         new_room.current_occupant_id = data["tenant_id"]
                
        #     return {"message": f"Room switch successful. Tenant id { tenant.id }, { tenant.name } switched from room { old_room.room_number } to room { new_room.room_number } on { str (switch_date) }."}, 201
            
        # except Exception as e:
        #     db.session.rollback()
        #     return {"error": str(e)}, 500

        try :

            required_fields = [ "tenant_id", "room_id", "agreed_rent" ]
            for field in required_fields :
                if field not in data :
                    return { "error" : f"{ field } is required." }, 400
            
            # Verify tenant exists.
            tenant = Tenant.query.get ( data [ "tenant_id" ] )
            if not tenant :
                return { "error" : "Tenant not found." }, 404
            
            # Verify tenant has existing occupancy.
            active_occupancy = Occupancy.query.filter (
                    Occupancy.tenant_id == data [ "tenant_id" ],
                    Occupancy.end_date == None
            ).first ()

            if not active_occupancy :
                return { "error" : "Tenant has no active occupancy. Please use the check-in endpoint to create a new tenant and occupancy." }, 409
            
            # Verify room availability
            new_room = Room.query.get ( data [ "room_id" ] )
            # if not new_room or new_room.status != "available" :
            #     return { "error" : "Room not available."}, 409
            
            if not room :
                return { "error" : "Not an existing room" }, 409

            if room.status != "available" :
                return { "error" : "Room has been booked." }, 409
            
            # Prevent switching to same room.
            if new_room.id == active_occupancy.room_id :
                return { "error" : "Tenant is already occupying this room." }, 409
            
            try :
                switch_date = datetime.utcnow().date()
            
            except Exception as e :
                return { "error" : "Invalid date format for start_date. Use ISO format (YYYY-MM-DD)." }, 400
            
            # Get old room
            old_room = Room.query.get ( active_occupancy.room_id )

            # End current occupancy.
            active_occupancy.end_date = switch_date
            if "damages_or_dues" in data :
                active_occupancy.damages_or_dues = data [ "damages_or_dues" ]
            if "damages_reason" in data :
                active_occupancy.damages_reason = data [ "damages_reason" ]

            active_occupancy.check_out_notes = data.get ( "check_out_notes", f"Tenant switched to room { new_room.room_number } on { switch_date }." )

            # Mark old room as available.
            old_room.status = "available"
            old_room.current_occupant_id = None
            

            # Create new occupancy.
            new_occupancy = Occupancy (
                tenant_id = data [ "tenant_id" ],
                room_id = data [ "room_id" ],
                agreed_rent = data [ "agreed_rent" ],
                start_date = switch_date,
                check_in_notes = data.get ( "check_in_notes", f"Tenant switched from room { old_room.room_number } on { str (switch_date) }." )
            )

            db.session.add ( new_occupancy )

            # Update new room.
            new_room.status = "occupied"
            new_room.current_occupant_id = data [ "tenant_id" ]

            db.session.commit ()

            return {
                "type" : "room_switch",
                # "tenant" : tenant.to_dict (),
                # "old_occupancy" : active_occupancy.to_dict (),
                # "old_room" : old_room.to_dict (),
                # "new_occupancy" : new_occupancy.to_dict (),
                # "new_room" : new_room.to_dict (),
                "message" : f"Tenant id { tenant.id }, { tenant.name } switched from room { old_room.room_number } to room { new_room.room_number } on { str (switch_date) }."
            }, 201
        
        except Exception as e :
            db.session.rollback()
            return { "error" : str (e) }, 500

            
            


class TenantDetails ( Resource ) :
    # /api/tenants/<int:tenant_id>

    # Retireve specific tenant and details.
    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self, tenant_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

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
            "room_number" : tenant.occupancies [ -1 ].room.room_number if tenant.occupancies else None, # Get the room number of the most recent occupancy if it exists, otherwise return None. Occupancies are ordered by start_date, so the most recent occupancy will be the last one in the list. [-1] takes the last element of the list.
            "occupancy_start_date" : str (tenant.occupancies [ -1 ].start_date) if tenant.occupancies else None,

            "created_at" : str (tenant.created_at)
        }, 200

    # Update tenant details (name, email, phone, national_id). Work on how to update occupancy details if tenant details are updated. Maybe create a separate endpoint for updating occupancy details.

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def put ( self, tenant_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403
        
        try :

            tenant = Tenant.query.get ( tenant_id )

            if not tenant :
                return { "error" : "Tenant not found." }, 404
            
            data = request.get_json ()


            # GET DATA FROM USER
            # tenant.name = data.get ( "name", tenant.name )
            if data.get ( "name" ) :
                if tenant.name == data [ "name" ] or Tenant.query.filter_by ( name = data [ "name" ]).first() :
                    return { "error" : "Tenant with this name already exists." }, 400
                else :
                    tenant.name = data [ "name" ]

            # tenant.email = data.get ( "email", tenant.email )
            if data.get ( "email" ) :
                if tenant.email == data [ "email" ] or Tenant.query.filter_by ( email = data [ "email" ]).first () :
                    return { "error" : "Email already exists." }, 400
                else :
                    tenant.email = data [ "email" ]


            # tenant.phone = data.get ( "phone", tenant.phone )
            if data.get ( "phone" ) :
                if tenant.phone == data [ "phone" ] or Tenant.query.filter_by ( 
                    phone = data [ "phone" ]).first () :
                    return { "error" : "Phone number already exists." }, 400
                else :
                    tenant.phone = data [ "phone" ]
                    
            # tenant.national_id = data.get ( "national_id", tenant.national_id )
            if data.get ( "national_id" ) :
                if tenant.national_id == data [ "national_id" ] or Tenant.query.filter_by ( national_id = data [ "national_id" ]).first () :
                    return { "error" : "Tenant with this national_id number already exists." }, 400
                else :
                    tenant.national_id = data [ "national_id" ]

            db.session.commit ()

            return { "message" : f"Tenant id { tenant.id }, { tenant.name } updated successfully." }, 200
        
        except Exception as e :
            db.session.rollback()
            return { "error" : str (e) }, 500
    
    # Delete tenant. Work on how to handle occupancy and billing details when a tenant is deleted. Maybe set occupancy end date to current date and mark all future billings as cancelled or delete them.
    # Theory : Delete tenant, set occupancy end date to current date, delete all future billings. This way we maintain historical data for past occupancies and billings while ensuring that no future charges are generated for the deleted tenant.

    # Admin required.
    # @token_required
    # @admin_required
    # def delete ( self, tenant_id ) :

    #     admin = require_admin ()

    #     if not admin :
    #         return { "error" : "Admin access required." }, 403

    #     tenant = Tenant.query.get ( tenant_id )

    #     if not tenant :
    #         return { "error" : "Tenant not found." }, 404
        
    #     # occupancy = tenant.occupancies [-1] if tenant.occupancies else None
    #     # if occupancy.end_date :
    #     #     return { "message" : "Delete occupancy before"}
        
    #     db.session.delete ( tenant )
    #     db.session.commit ()

    #     return { "message" : "Tenant deleted successfully." }, 200



# Retrieves a tenant's list of occupancies. This will allow us to show the tenant's current and past occupancies when we retrieve their details.
class TenantOccupancies ( Resource ) :
    # /api/tenants/<int:tenant_id>/occupancies

    # Manager required.
    # @token_required
    # @manager_required
    def get ( self, tenant_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        occupancies = tenant.occupancies

        return [ {
            "id" : o.id,
            "tenant_id" : o.tenant.id,
            "tenant_name" : o.tenant.name,
            "room_id" : o.room_id,
            "room_number" : o.room.room_number,
            "agreed_rent" : int (o.agreed_rent),
            "start_date" : str (o.start_date),
            "end_date" : str (o.end_date) if o.end_date else None,
            "damages_or_dues" : int (o.damages_or_dues) if o.damages_or_dues else 0,
            "damages_reason" : o.damages_reason if o.damages_reason else None,
            "check_in_notes" : o.check_in_notes if o.check_in_notes else None,
            "check_out_notes" : o.check_out_notes if o.check_out_notes else None,
        } for o in occupancies ], 200
    


# Retrieve a tenant's active occupancy, all monthly charges, all payments and running balances. 
class TenantLedger ( Resource ) :
    # /api/tenants/<int:tenant_id>/ledger

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self, tenant_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

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
                    "occupancy_id" : o.id,
                    "tenant_name" : tenant.name,
                    "room_number" : o.room.room_number,
                    "type" : "charge",
                    "monthly_charge_id" : c.id,
                    "amount" : int (c.rent_amount + c.water_bill),
                    "date" : str (c.charge_date)
                } )
            
            for p in payments :
                ledger.append ( {
                    "occupancy_id" : o.id,
                    "tenant_name" : tenant.name,
                    "room_number" : o.room.room_number,
                    "type" : "payment",
                    "payment_id" : p.id,
                    "monthly_charge_id" : p.monthly_charge_id,
                    "amount" : int (p.amount),
                    "date" : str (p.payment_date)
                } )
        
        # Sort the ledger by date.
        ledger.sort ( key = lambda x : x [ "date" ] )

        # Get the difference of charges and payments to calculate the running balance.
        balance = 0
        for entry in ledger :

            # Add charges to balance and subtract payments from balance.

            if entry [ "type" ] == "charge" :
                balance += entry [ "amount" ]

            elif entry [ "type" ] == "payment" :
                balance -= entry [ "amount" ]
            
            entry [ "running_balance" ] = balance

        return ledger, 200