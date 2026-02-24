
from flask import request, jsonify
from flask_restful import Resource
from auth.permissions import admin_required, manager_required
from auth.jwt import token_required
from models import db, Payment, MonthlyCharge
from datetime import datetime


class PaymentsList ( Resource ) :

    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self ) :

        payments = Payment.query.all()

        return [ {
            "id" : p.id,
            "tenant_id" : p.tenant_id,
            "monthly_charge_id" : p.monthly_charge_id,
            "amount" : p.amount,
            "method" : p.method,
            "payment_date" : p.payment_date
        } for p in payments ], 200


class RecordPayment ( Resource ) :

    # Admin/ Manager required.
    @token_required
    @manager_required
    def post ( self ) :

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

        return { "message" : "Payment recorded." }, 201


class PaymentDetails ( Resource ) :

    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self, payment_id ) :

        payment = Payment.query.get ( payment_id )

        if not payment :
            return { "error" : "Payment not found" }, 404
        
        return {
            "id" : payment.id,
            "tenant_id" : payment.tenant_id,
            "monthly_charge_id" : payment.monthly_charge_id,
            "amount" : payment.amount,
            "method" : payment.method,
            "payment_date" : payment.payment_date.isoformat(),
            "created_at" : payment.created_at.isoformat()
        }