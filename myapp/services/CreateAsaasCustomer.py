from flask import Flask, request, jsonify, blueprints
import requests
from typing import Tuple, Dict ,Any
from config import Config

URL_API = Config.URL_API
SANDBOX_URL_API = Config.SANDBOX_URL_API

API_TOKEN = Config.API_TOKEN
SANDBOX_API_TOKEN = Config.SANDBOX_API_TOKEN
ASAAS_WALLET_ID = Config.ASAAS_WALLET_ID

INTERNAL_TOKEN_API = Config.INTERNAL_TOKEN_API


#HELP func create_asaas_customer
def create_asaas_customer(user: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:

    if (not user["customer_id"] is None):
        return 400, {
            "errors": "user already has asaas_id"
        }

    required = [
        ("usename", user["username"]),
        ("cpf", user["cpf"]),
    ]
    undefined = [key for key, value in required if value is None]
    if undefined:
        return 400, {
            "status": 400,
            "description": "user parameter not defined", 
            "errors": undefined
        }
    
    payload = {
        "name": user["username"],
        "email": user["email"],
        "cpfCnpj": user["cpf"],
    }

    header = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": SANDBOX_API_TOKEN
    }

    URL = SANDBOX_URL_API + "/customers"

    response = requests.post(URL, json = payload, headers = header)


    if (response.status_code != 200):
        return response.status_code, {
            "status": response.status_code, "description": response.errors
        }

    response_data = response.json()
    user["customer_id"] = response_data.get("id")
    return response.status_code, {
        "status": response.status_code, "description": response_data
    }


