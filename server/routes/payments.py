
from flask import request, jsonify
from models import db, Payment, MonthlyCharge
from datetime import datetime


class PaymentResource ( Resource ) :

    def get_payments () :

        pass


    def record_payment () :

        data = request.getjson ()
        
        pass

