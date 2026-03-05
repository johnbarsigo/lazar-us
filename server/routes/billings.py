
from flask import request, jsonify
from flask_restful import Resource
# from auth.permissions import admin_required, manager_required
# from auth.jwt import token_required
from auth.permissions import require_admin, require_manager
from models import db, MonthlyCharge, Occupancy
from datetime import date


class GenerateMonthlyBillings ( Resource ) :
    # /api/billings/generate

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def post ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        data = request.get_json()

        month  = data [ "month" ]
        year = data [ "year" ]

        active_occupancies = Occupancy.query.filter ( Occupancy.end_date == None ).all()

        # Counter for number of billings created.
        created = 0

        for o in active_occupancies :
            existing = MonthlyCharge.query.filter_by (
                occupancy_id = o.id,
                month = month,
                year = year
            ).first()

            if existing :
                continue

            charge = MonthlyCharge (
                occupancy_id = o.id,
                month = month,
                year = year,
                rent_amount = o.agreed_rent,
                water_bill = data.get ( "water_bill", 0 ),
                charge_date = date.today(),
                total_amount = o.agreed_rent + data.get ( "water_bill", 0 ),
                created_at = date.today()
            )

            db.session.add ( charge )
            created +=1
        
        db.session.commit ()

        return { "message" : f" {created} monthly charges created. " }, 201



class BillingsList ( Resource ) :
    # /api/billings

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        billings = MonthlyCharge.query.all()

        return [ {
            "id" : b.id,
            "occupancy_id" : b.occupancy_id,
            "month" : b.month,
            "year" : b.year,
            "rent_amount" : int (b.rent_amount),
            "water_bill" : int (b.water_bill)
        } for b in billings ], 200



class BillingDetails ( Resource ) :
    # /api/billings/<int:billing_id>

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self, billing_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        billing = MonthlyCharge.query.get ( billing_id )

        if not billing :
            return { "error" : "Billing record not found." }, 404
        
        return {
            "id" : billing.id,
            "occupancy_id" : billing.occupancy_id,
            "month" : billing.month,
            "year" : billing.year,
            "rent_amount" : int (billing.rent_amount),
            "water_bill" : int (billing.water_bill),
            # "other_charges" : billing.other_charges,
            "charge_date" : str (billing.charge_date.isoformat()),
            "created_at" : str (billing.created_at.isoformat())
        }, 200
    

    def put ( self, billing_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        billing = MonthlyCharge.query.get ( billing_id )

        if not billing :
            return { "error" : "Billing record not found." }, 404
        
        data = request.get_json()

        billing.rent_amount = data.get ( "rent_amount", billing.rent_amount )
        billing.water_bill = data.get ( "water_bill", billing.water_bill )
        billing.updated_at = datetime.utcnow()

        db.session.commit ()

        return { "message" : f"Billing record updated at {billing.updated_at} successfully." }, 200
    

    def delete ( self, billing_id ) :

        admin = require_admin ()

        if not admin :
            return { "error" : "Admin access required." }, 403
        
        billing = MonthlyCharge.query.get ( billing_id )

        if not billing :
            return { "error" : "Billing record not found." }, 404

        db.session.delete ( billing )
        db.session.commit ()

        return { "message" : "Billing record deleted successfully." }, 200