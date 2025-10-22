from myapp.setup.InitSqlAlchemy import db
from myapp.models.Payments import payments
from myapp.models.Users import users
from flask import Blueprint, jsonify, request
from typing import  Dict, Tuple, Any
from config import Config

INTERNAL_TOKEN_API = Config.INTERNAL_TOKEN_API
ASAAS_USER_ID =  1 #ID OF ASSAS USER
webhook = Blueprint("webhook", __name__)


@webhook.route('/payment/webhook', methods=['POST'])
def payments_webhook() -> Tuple[Dict[str, bool], int]:
    body = request.json
    received_token = request.headers.get("asaas-access-token", None)
    if (not received_token):
        return jsonify({"received": True}), 400

    if (received_token != INTERNAL_TOKEN_API):
        return jsonify({"received": True}), 400
    
    payment_data = body.get("payment")
    asaas_payment_id = payment_data.get("id")
    customer_id = payment_data.get("customer")
    value = payment_data.get("value")
    date_created = body.get("dateCreated")
    status = payment_data.get("status")

    payment = payments.query.filter(payments.asaas_payment_id == asaas_payment_id)

    payment_event = body.get("event")

    user = users.query.filter(users.api_token == customer_id)

    data = {
            "amount":                   value,
            "opening_datetime":         date_created,
            "due_datetime":             payment_data.get("dueDate"),
            #"confirmation_datetime":    payment_data.get(),
            "payer_user_id":            ASAAS_USER_ID,
            "payee_user_id":            user.user_id,
            "payment_method":           payment_data.get("billingType"),
            "payment_status":           status,
            "asaas_payment_id":         asaas_payment_id
        }

    if (payment_event == "PAYMENT_RECEIVED"):
        user.wallet += value*100
        data["confirmation_datetime"] = date_created
        db.session.commit()
        

    if(not payment):
        payments.save_item(data)
        return jsonify({"received": True}), 201

    payment.set_status(status)
    return jsonify({"received": True}), 200