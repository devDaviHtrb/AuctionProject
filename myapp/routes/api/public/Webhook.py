from flask import Blueprint, jsonify, request

from typing import  Dict
from config import Config

INTERNAL_TOKEN_API = Config.INTERNAL_TOKEN_API
webhook = Blueprint("payment", __name__, url_prefix = "/payment")


@webhook.route('/webhook', methods=['POST'])
def payments_webhook() -> Dict[str, bool]:
    body = request.json
    received_token = request.headers.get("asaas-access-token")

    print(request.headers, INTERNAL_TOKEN_API)

    if (received_token != INTERNAL_TOKEN_API):
        return jsonify({"received": False})

    if (body['event'] == 'PAYMENT_RECEIVED'):
        payment = body['payment']
        #receive_payment(payment)

    return jsonify({"received": True})