
from flask import request
from flask_restful import Resource
from auth.jwt import decode_token
from auth.permissions import admin_required, manager_required
from models import db, Occupancy, Tenant, Room


# Retrieve a list of all occupancies and details.
class Occupancies ( Resource ) :

    @token_required
    def get ( self ) :

        occupancies = Occupancy.query.all()

        return [ {
            "id" : o.id,
            "tenant_id" : o.tenant_id,
            "room_id" : o.room_id,
            "rent_amount" : o.rent_amount,
            "water_bill" : o.water_bill,
            "other_charges" : o.other_charges,
            "total_amount" : o.rent_amount + o.water_bill + o.other_charges,
            "charge_date" : o.charge_date
        } for o in occupancies ], 200


class OccupancyDetails ( Resource ) :

    @token_required
    def get ( self, occupancy_id ) :

        occupancy = Occupancy.query.get ( occupancy_id )

        if not occupancy :
            return { "error" : "Occupancy not found." }, 404
        
        return {
            "id" : occupancy.id,
            "tenant_id" : occupancy.tenant_id,
            "room_id" : occupancy.room_id,
            "rent_amount" : occupancy.rent_amount,
            "water_bill" : occupancy.water_bill,
            "other_charges" : occupancy.other_charges,
            "total_amount" : occupancy.rent_amount + occupancy.water_bill + occupancy.other_charges,
            "charge_date" : occupancy.charge_date
        }, 200
    

    # We can also add an endpoint to update the occupancy details. This will allow us to update the rent amount, water bill and other charges for an existing occupancy. This will be useful when we want to make adjustments to the charges for a tenant's occupancy.
    @token_required
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
    
    # We can also add an endpoint to delete an occupancy. This will allow us to remove an occupancy record when a tenant moves out or when we want to clear up old records. We should also consider whether we want to delete the associated monthly charges and payments when we delete an occupancy, or if we want to keep them for historical records. For now, we will just delete the occupancy and keep the associated charges and payments.
    @token_required
    def delete ( self, occupancy_id ) :

        occupancy = Occupancy.query.get ( occupancy_id )

        if not occupancy :
            return { "error" : "Occupancy not found." }, 404
        
        db.session.delete ( occupancy )
        db.session.commit ()
        return { "message" : "Occupancy deleted successfully." }, 200
    

class CreateOccupancy ( Resource ) :

    @token_required
    def post ( self ) :

        data = request.get_json ()

        tenant_id = data.get ( "tenant_id" )
        room_id = data.get ( "room_id" )
        rent_amount = data.get ( "rent_amount" )
        water_bill = data.get ( "water_bill" )
        other_charges = data.get ( "other_charges", 0.0 )
        charge_date = data.get ( "charge_date" )

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        room = Room.query.get ( room_id )

        if not room :
            return { "error" : "Room not found." }, 404
        
        occupancy = Occupancy (
            tenant_id = tenant_id,
            room_id = room_id,
            rent_amount = rent_amount,
            water_bill = water_bill,
            other_charges = other_charges,
            charge_date = charge_date
        )

        db.session.add ( occupancy )
        db.session.commit ()

        return {
            "message" : "Occupancy created successfully.",
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
        }, 201
