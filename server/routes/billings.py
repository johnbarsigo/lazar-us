
from flask import request, jsonify
from flask_restful import Resource
from models import db, MonthlyCharge, Occupancy
from datetime import date


class BillingResource ( Resource ) :

    def generate_monthly_billings () :

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
                water_bill = MonthlyCharge.water_bill
            )

            db.session.add ( charge )
            created +=1
        
        db.session.commit ()

        return { "message" : f" {created} monthly charges created. " }


        pass


    def get_all_billings () :

        pass