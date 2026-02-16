
from flask import request, jsonify
from models import db, Payment, MonthlyCharge
from datetime import datetime


class PaymentResource ( Resource ) :

    def get_payments ( self ) :

        pass


    def record_payment () :

        data = request.get_json ()

        charge = MonthlyCharge.query.get ( data [ "monthly_charge_id" ] )

        if not charge :
            return { "error" : "Charge not found." }, 404
        
        payment = Payment (
            tenant_id = charge.occupancy.tenant_id,
            monthly_charge_id = charge.id,
            amount = data [ "amount" ],
            method = data [ "method" ],
            payment_date = datetime.strptime ( data [ "payment_date" ], "%Y-%m-%d" )
        )

        db.session.add ( payment )
        db.session.commit ()

        return { "message" : "Payment recorded." }

        pass


api.add_resource ( PaymentResource, "/api/payments/record" )

