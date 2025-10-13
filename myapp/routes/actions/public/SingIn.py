from flask import Blueprint, jsonify, url_for, request, Response

from myapp.services.CreateUser import create_user
from myapp.utils.Validations.validations import *
from myapp.utils.utils import uploadImage

from typing import Tuple


singIn = Blueprint("singIn", __name__)
datakey = [
    "username",
    "password",
    "email",
    "cpf",
    "name",
    "userType",
    "cellphone1",
    "cellphone2",
    "landline",
    "photo", 
    "street_name", 
    "street_number", 
    "apt",
    "zip_code",
    "district",
    "city",
    "state"
]
nullAbleValues = [
    "cellphone2",
    "cnpj",
    "cpf", 
    "rg", 
    "photo",
    "landline",
    "scrap_purchase_authorization"
]
nullAbleValues += [
    "cellphone1",
    "landline",
    "street_name",
    "street_number",
    "apt",
    "zip_code",
    "district",
    "city",
    "state"
]

@singIn.route("/singIn", methods=["POST"])
def SingIn() -> Tuple[Response, int]:
    user_type = request.form.get("userType", "physical_person")#legal_person or physical_person
    
    datakey += [
        "rg",
        "birth_date",
        "gender"
    ] if user_type == "physical_person" else [
        "cnpj", 
        "state_tax_registration",
        "legal_business_name",
        "trade_name",
        "scrap_purchase_authorization"
    ]
    

    data = {}
    missingInfo = []
    for requiredData in datakey:
        value = request.form.get(requiredData, None)
        if value == "" or value is None and requiredData not in nullAbleValues:
            msg = "Complete all the inputs"
            missingInfo.append(requiredData)
        else:
            data[requiredData] = value

    if missingInfo:
        return jsonify({"InputError": msg, "MissingInformation": missingInfo}), 400
        
    #validations
    if not is_email(data["email"]):
        msg = "Invalid email"
        return jsonify({"InputError": msg}), 400
    
    if data.get("cellphone1", None):
        if not is_phone_number(data["cellphone1"]) or ( not is_phone_number(data["cellphone2"]) and data["cellphone2"] != "") or (not is_phone_number(data["landline"]) and data["landline"]!= ""):
            msg = "Invalid chellphone"
            return jsonify({"InputError": msg}), 400
        
    if data.get("zip_code", None) and data.get("district", None) and data.get("state", None) and data.get("city", None):
        if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]): #without contractions
            msg = "Invalid location data"
            return jsonify({"InputError": msg}), 400
    
    if data.get("photo"):
        if validateImg(data["photo"]):
            photo_url = uploadImage(data["photo"], "Users_photos")
            if not photo_url:
                msg = "Image db connection error, sorry, try the submit without img"
                print("Db connection error")
            else: data["photo_url"] = photo_url
        else:
            msg = "Invalid file "
            return jsonify({"InputError": msg}), 400

    
    if user_type == "physical_person" and data.get("cpf", None) and data.get("rg", None):
            if is_cpf(data["cpf"]) and is_rg(data["rg"]):
                if not User_validation(data["username"], data["email"], data["cpf"],rg=data["rg"]):
                    msg = "There is already a user with that name, email, CPF or Rg"
                    return  jsonify({"InputError": msg}), 400
            else:
                msg = "Invalid CPF"
                return  jsonify({"InputError": msg}), 400
            
    elif data.get("cnpj", None):
        if is_cnpj(data["cnpj"]) and state_tax_registration_validation(data["state_tax_registration"], data["state"]):
            if not User_validation(data["username"], data["email"], data["cpf"], cnpj=data["cnpj"]):
                msg = "There is already a user with that name, email or CNPJ"
                return  jsonify({"InputError": msg}), 400
        else:
            msg = "Invalid CNPJ or state_tax_registration"
            return  jsonify({"InputError": msg}), 400
        
    create_user(data)

    
    return jsonify({"redirect":url_for("loginPage.LoginPage"), "Data": data}), 201

