
from flask import request, jsonify
from flask_restful import Resource
from models import db, MonthlyCharge, Occupancy
from datetime import date


class GenerateMonthlyBillings ( Resource ) :

    def post ( self ) :

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
                water_bill = data.get ( "water_bill", 0 )
            )

            db.session.add ( charge )
            created +=1
        
        db.session.commit ()

        return { "message" : f" {created} monthly charges created. " }, 201



class BillingsList ( Resource ) :

    def get ( self ) :

        billings = MonthlyCharge.query.all()

        return [ {
            "id" : b.id,
            "occupancy_id" : b.occupancy_id,
            "month" : b.month,
            "year" : b.year,
            "rent_amount" : b.rent_amount,
            "water_bill" : b.water_bill
        } for b in billings ], 200


api.add_resource ( GenerateMonthlyBillings, "/api/billings/generate" )
api.add_resource ( BillingsList, "/api/billings" )