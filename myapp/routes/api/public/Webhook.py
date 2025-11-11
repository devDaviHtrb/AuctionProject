from myapp.setup.InitSqlAlchemy import db
import myapp.repositories.PaymentRepository as payments_repository
import myapp.repositories.UserRepository as user_repository
from flask import Blueprint, jsonify, request
from typing import  Dict, Tuple
from myapp.config import Config

INTERNAL_TOKEN_API =    Config.INTERNAL_TOKEN_API
ASAAS_USER_ID =         1 #ID OF ASSAS USER, SORRY :(
webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route('/payment/webhook', methods=['POST'])
def payments_webhook() -> Tuple[Dict[str, bool], int]:
    body = request.json
    received_token = request.headers.get("asaas-access-token", None)
    if (not received_token):
        return jsonify({"received": False}), 400

    if (received_token != INTERNAL_TOKEN_API):
        return jsonify({"received": False}), 400
    
    payment_data = body.get("payment")
    asaas_payment_id = payment_data.get("id")
    customer_id = payment_data.get("customer")
    value = payment_data.get("value")
    date_created = body.get("dateCreated")
    status = payment_data.get("status")

    payment = payments_repository.get_by_id(asaas_payment_id)

    payment_event = body.get("event")

    user = user_repository.get_by_api_token(customer_id)

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
        user.wallet += value
        data["confirmation_datetime"] = date_created
        db.session.commit()
        

    if(not payment):
        payments_repository.save_item(data)
        return jsonify({"received": True}), 201

    payments_repository.set_status(payment, status)
    return jsonify({"received": True}), 200