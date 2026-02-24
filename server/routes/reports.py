
from flask import request, jsonify
from flask_restful import Resource
from auth.jwt import decode_token
from auth.permissions import admin_required, manager_required
from auth.jwt import token_required
from models import db, Tenant, Occupancy, MonthlyCharge, Payment
from sqlalchemy import func


class GenerateArrearsReport ( Resource ) :

    # Admin/ Manager required.
    @token_required
    @manager_required
    def get ( self ) :

        results = db.session.query (
            Tenant.id,
            Tenant.name,
            func.sum (MonthlyCharge.rent_amount + MonthlyCharge.water_bill ).label ( "total_billed" ),
            func.coalesce ( func.sum ( Payment.amount ), 0 ).label ( "total_paid" )
        ).join ( Occupancy, Occupancy.tenant_id == Tenant.id ) \
        .join ( MonthlyCharge, MonthlyCharge.occupancy_id == Occupancy.id ) \
        .outerjoin ( Payment, Payment.monthly_charge_id == MonthlyCharge.id ) \
        .group_by ( Tenant.id ).all()

        report = []

        for r in results :
            balance = float ( r.total_billed) - float ( r.total_paid )

            if balance > 0 :
                report.append ( {
                    "tenant_id" : r.id,
                    "name" : r.name,
                    "total billed" : float ( r.total_billed ),
                    "total_paid" : float ( r.total_paid ),
                    "balance" : balance
                } )
        
        return report