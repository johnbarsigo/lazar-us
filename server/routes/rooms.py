
from flask import request
from flask_restful import Resource
from models import db, Room, Tenant
from datetime import datetime


class RoomsList ( Resource ) :

    def get ( self ) :

        rooms = Room.query.all()

        return [ {
            "id" : r.id,
            "room_number" : r.room_number,
            "default_rent" : r.default_rent,
            "capacity" : r.capacity,
            "status" : r.status,
            "current_occupants" : len ( r.occupancies ),
            "created_at" : r.created_at
        } for r in rooms ], 200