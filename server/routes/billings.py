
from flask import request, jsonify
from models import db, MonthlyCharge, Occupancy
from datetime import date