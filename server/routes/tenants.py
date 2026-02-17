
from flask import request
from flask_restful import Resource
from models import db, Tenant
from datetime import datetime


class TenantsList ( Resource ) :

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

        return { "message" : f"Tenant id { tenant.id } and name { tenant.name } created successfully." }, 201