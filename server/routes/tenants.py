
from flask import request
from flask_restful import Resource
from models import db, Tenant
from datetime import datetime


class TenantsList ( Resource ) :

    # Retrieve all tenants and details.
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
class CreateTenant ( Resource ) :

    def post ( self ) :

        data = request.get_json ()

        tenant = Tenant (
            name = data [ "name" ],
            email = data [ "email" ],
            phone = data [ "phone" ],
            national_id = data [ "national_id" ]
        )

        db.session.add ( tenant )
        db.session.commit ()

        return { "message" : f"Tenant id { tenant.id }, { tenant.name } created successfully." }, 201


class TenantDetails ( Resource ) :

    # Retireve specific tenant and details.
    def get ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        return {
            "id" : tenant.id,
            "name" : tenant.name,
            "email" : tenant.email,
            "phone number" : tenant.phone,
            "national_id" : tenant.national_id,
            "created_at" : tenant.created_at
        }, 200

    # Update tenant details (name, email, phone, national_id). Work on how to update occupancy details if tenant details are updated. Maybe create a separate endpoint for updating occupancy details.
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
    def delete ( self, tenant_id ) :

        tenant = Tenant.query.get ( tenant_id )

        if not tenant :
            return { "error" : "Tenant not found." }, 404
        
        db.session.delete ( tenant )
        db.session.commit ()

        return { "message" : "Tenant deleted successfully." }, 200