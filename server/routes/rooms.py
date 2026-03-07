
from flask import request
from flask_restful import Resource
# from auth.permissions import admin_required, manager_required
# from auth.jwt import token_required
from auth.permissions import require_admin, require_manager
from models import db, Room, Tenant
from datetime import datetime


class RoomsList ( Resource ) :

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        rooms = Room.query.all()

        return [ {
            "id" : r.id,
            "room_number" : r.room_number,
            "default_rent" :int( r.default_rent ),
            "capacity" : r.capacity,
            "status" : r.status,
            "current_occupants" : len ( r.occupancies ),
            "created_at" : str(r.created_at)
        } for r in rooms ], 200
    


class RoomDetails ( Resource ) :

    # Admin/ Manager required.
    # @token_required
    # @manager_required
    def get ( self, room_id ) :

        manager = require_manager ()

        if not manager :
            return { "error" : "Unauthorized. Manager access required." }, 403

        room = Room.query.get ( room_id )

        if not room :
            return { "error" : "Room not found." }, 404
        
        occupants = [ {
            "tenant_id" : o.tenant_id,
            "tenant_name" : o.tenant.name,
            "start_date" : str (o.start_date),
            "end_date" : str (o.end_date)
        } for o in room.occupancies ]

        return {
            "id" : room.id,
            "room_number" : room.room_number,
            "default_rent" : int (room.default_rent),
            "capacity" : room.capacity,
            "status" : room.status,
            "current_occupants" : occupants,
            "created_at" : str(room.created_at)
        }, 200
    

        # Admin required.
    # @token_required
    # @admin_required
    def post ( self ) :

        data = request.get_json ()

        room = Room (
            room_number = data [ "room_number" ],
            default_rent = data [ "default_rent" ],
            capacity = data [ "capacity" ],
            created_at = datetime.utcnow(),
            status = "available"
        )

        db.session.add ( room )
        db.session.commit ()

        return { "message" : f"Room { room.room_number } created successfully." }, 201

    # Admin required.
    # @token_required
    # @admin_required
    def delete ( self, room_id ) :

        room = Room.query.get ( room_id )

        if not room :
            return { "error" : "Room not found." }, 404
        
        db.session.delete ( room )
        db.session.commit ()

        return { "message" : "Room deleted successfully." }, 200