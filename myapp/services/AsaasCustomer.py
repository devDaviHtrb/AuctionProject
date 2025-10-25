from myapp.models.Users import users
import myapp.repositories.UserRepository as user_repository
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
def create_asaas_customer(user_id:int) -> Tuple[Dict[str, Any], int]:
    user = users.query.get(user_id)
    if (not user):
        return {
            "description": "user does not exist"
        }, 400 
    customer_id = user.api_token
    if (customer_id):
        return {
            "description": "user already has asaas_id"
        }, 400
    user_document = user.cpf
    if (not user_document):
        return {
            "description": "user parameter not defined", 
        }, 400
    
    username = user.username
    email = user.email
    
    payload = {
        "name":     username,
        "email":    email,
        "cpfCnpj":  user_document,
    }

    header = {
        "accept":       "application/json",
        "content-type": "application/json",
        "access_token": SANDBOX_API_TOKEN
    }

    URL = SANDBOX_URL_API + "/customers"

    response = requests.post(
        URL,
        json =      payload,
        headers =   header
    )


    if (response.status_code != 200):
        return {
            "description": response.errors
        }, response.status_code, 

    response_data = response.json()
    user_repository.set_api_token(
        user,
        response_data.get("id")
        )
    return {
        "description": response_data
    }, response.status_code, 


