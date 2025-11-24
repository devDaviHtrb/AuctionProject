from myapp.setup.InitSqlAlchemy import db
from flask import Blueprint, jsonify, request, Response
from typing import  Dict, Tuple
from myapp.config import Config
import myapp.repositories.UserRepository as user_repository
import myapp.repositories.PaymentRepository as payments_repository
import myapp.repositories.PaymentMethodRepository as payment_method_repository
import requests


#===================== API =====================
URL_API =               Config.URL_API
SANDBOX_URL_API =       Config.SANDBOX_URL_API
API_TOKEN =             Config.API_TOKEN
SANDBOX_API_TOKEN =     Config.SANDBOX_API_TOKEN
ASAAS_WALLET_ID =       Config.ASAAS_WALLET_ID
INTERNAL_TOKEN_API =    Config.INTERNAL_TOKEN_API
ASAAS_USER_ID =         1#ID OF ASSAS USER,SORRY
#================================================

PAYMENT_RECEIVED = "PAYMENT_RECEIVED"

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route('/payment/webhook', methods=['POST'])
def payments_webhook() -> Tuple[Response, int]:
    body = request.json
    received_token = request.headers.get("asaas-access-token", None)
    if (not received_token):
        return jsonify({"received": False, "error": "No Received Token"}), 400

    if (received_token != INTERNAL_TOKEN_API):
        return jsonify({"received": False, "error": "Invalid Token"}), 400
    
    payment_data = body.get("payment")
    asaas_payment_id = payment_data.get("id")
    customer_id = payment_data.get("customer")
    value = payment_data.get("value")
    date_created = body.get("dateCreated")

    method = payment_data.get("billingType")

    payment = payments_repository.get_by_asaas_id(asaas_payment_id)

    payment_event = body.get("event")

    status = payment_event

    url = SANDBOX_URL_API + f"/customers/{customer_id}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": SANDBOX_API_TOKEN
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    user_doc =      response_data.get("cpfCnpj", None)
    user_email =    response_data.get("email", None)


    user = None
    if(user_doc):
        user = user_repository.get_by_cpf(user_doc)
    if(user_email and not user):
        user = user_repository.get_by_email(user_email)
    if(not user):
        return jsonify({"received": False, "error": "Not User"}), 400
    

    data = {
        "amount":                   value,
        "opening_datetime":         date_created,
        "due_date":                 payment_data.get("dueDate"),
        #"confirmation_datetime":   payment_data.get(),
        "payer_user_id":            ASAAS_USER_ID,
        "payee_user_id":            user.user_id,
        "payment_method":           method,
        "asaas_payment_id":         asaas_payment_id
    }

    if (payment_event.lower() == PAYMENT_RECEIVED.lower()):
        user.wallet += value
        if (not payment):
            data["confirmation_datetime"] = date_created
        else:
            payment.confirmation_datetime = date_created
        db.session.commit()
        

    code = 200
    if(not payment):
        payment = payments_repository.save_item(data)
        code = 201

    payments_repository.set_status(payment, status)
    return jsonify({"received": True}), code