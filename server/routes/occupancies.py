
from flask import request
from flask_restful import Resource
# from auth.permissions import admin_required, manager_required
# from auth.jwt import token_required
from auth.permissions import require_admin, require_manager
from models import db, Occupancy, Tenant, Room, MonthlyCharge
from datetime import datetime


# Retrieve a list of all occupancies and details.
class Occupancies ( Resource ) :

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        occupancies = Occupancy.query.all()

        return [ {
            "id" : o.id,
            "tenant_id" : o.tenant_id,
            "room_id" : o.room_id,
            "room_number" : o.room.room_number,
            "rent_amount" : int (o.agreed_rent),
            "start_date" : str (o.start_date),
            "end_date" : str (o.end_date) if o.end_date else None,
            "created_at" : str (o.created_at)
        } for o in occupancies ], 200


class OccupancyDetails ( Resource ) :

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self, occupancy_id ) :

        occupancy = Occupancy.query.get ( occupancy_id )
        monthly_charge = MonthlyCharge.query.filter_by ( occupancy_id = occupancy_id ).first()

        if not occupancy :
            return { "error" : "Occupancy not found." }, 404
        
        return {
            "id" : occupancy.id,
            "tenant_id" : occupancy.tenant_id,
            "room_id" : occupancy.room_id,
            "room_number" : occupancy.room.room_number,
            "rent_amount" : int (occupancy.agreed_rent),
            "start_date" : str (occupancy.start_date),
            "end_date" : str (occupancy.end_date) if occupancy.end_date else None,
            "water_bill" : int (monthly_charge.water_bill) if monthly_charge and monthly_charge.water_bill else 0,
            "total_amount" : int (occupancy.agreed_rent + (monthly_charge.water_bill if monthly_charge else 0)),
            "charge_date" : str (monthly_charge.charge_date.isoformat()) if monthly_charge else None,
            "created_at" : str (occupancy.created_at.isoformat())
        }, 200
    

    # We can also add an endpoint to update the occupancy details. This will allow us to update the rent amount, water bill and other charges for an existing occupancy. This will be useful when we want to make adjustments to the charges for a tenant's occupancy.
    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def put ( self, occupancy_id ) :

        occupancy = Occupancy.query.get ( occupancy_id )

        if not occupancy :
            return { "error" : "Occupancy not found." }, 404
        
        data = request.get_json ()

        occupancy.rent_amount = data.get ( "rent_amount", occupancy.rent_amount )
        occupancy.water_bill = data.get ( "water_bill", occupancy.water_bill )
        occupancy.other_charges = data.get ( "other_charges", occupancy.other_charges )
        db.session.commit ()
        return {
            "message" : "Occupancy details updated successfully.",
            "occupancy" : {
                "id" : occupancy.id,
                "tenant_id" : occupancy.tenant_id,
                "room_id" : occupancy.room_id,
                "rent_amount" : occupancy.rent_amount,
                "water_bill" : occupancy.water_bill,
                "other_charges" : occupancy.other_charges,
                "total_amount" : occupancy.rent_amount + occupancy.water_bill + occupancy.other_charges,
                "charge_date" : occupancy.charge_date
            }
        }, 200
    
    # We can also add an endpoint to delete an occupancy. This will allow us to remove an occupancy record when a tenant moves out or when we want to clear up old records. For now, we will just delete the occupancy and keep the associated charges and payments.
    # Admin required.
    # @token_required
    # @admin_required
    def delete ( self, occupancy_id ) :

        occupancy = Occupancy.query.get ( occupancy_id )

        if not occupancy :
            return { "error" : "Occupancy not found." }, 404
        
        db.session.delete ( occupancy )
        db.session.commit ()
        return { "message" : "Occupancy deleted successfully." }, 200
    

# class CreateOccupancy ( Resource ) :

#     # Admin/ Manager required.
#     @token_required
#     @manager_required
#     def post ( self ) :

#         data = request.get_json ()

#         tenant_id = data.get ( "tenant_id" )
#         room_id = data.get ( "room_id" )
#         rent_amount = data.get ( "rent_amount" )
#         water_bill = data.get ( "water_bill" )
#         other_charges = data.get ( "other_charges", 0.0 )
#         charge_date = data.get ( "charge_date" )

#         tenant = Tenant.query.get ( tenant_id )

#         if not tenant :
#             return { "error" : "Tenant not found." }, 404
        
#         room = Room.query.get ( room_id )

#         if not room :
#             return { "error" : "Room not found." }, 404
        
#         occupancy = Occupancy (
#             tenant_id = tenant_id,
#             room_id = room_id,
#             rent_amount = rent_amount,
#             water_bill = water_bill,
#             other_charges = other_charges,
#             charge_date = charge_date
#         )

#         db.session.add ( occupancy )
#         db.session.commit ()

#         return {
#             "message" : "Occupancy created successfully.",
#             "occupancy" : {
#                 "id" : occupancy.id,
#                 "tenant_id" : occupancy.tenant_id,
#                 "room_id" : occupancy.room_id,
#                 "rent_amount" : occupancy.rent_amount,
#                 "water_bill" : occupancy.water_bill,
#                 "other_charges" : occupancy.other_charges,
#                 "total_amount" : occupancy.rent_amount + occupancy.water_bill + occupancy.other_charges,
#                 "charge_date" : occupancy.charge_date
#             }
#         }, 201
