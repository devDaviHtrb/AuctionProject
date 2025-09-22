from flask import Blueprint, jsonify, redirect, url_for, request, Response

from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons
from myapp.models.Users import users

from myapp.services.CreateUser import create_user
from myapp.utils.Validations.UserValidation import User_validation
from myapp.utils.utils import get_columns_names, is_cpf, is_cnpj, is_email, User_validation, is_phone_number, is_rg, adress_validation, state_tax_registration_validation


singIn = Blueprint("singIn", __name__)

@singIn.route("/singIn", methods=["POST"])

def SingIn():
    user_type = request.form["userType"]#legal_person or physical_person


    #required data
    datakey = ["username","password","email","cpf","name","userType","cellphone1","cellphone2", "landline","photo", "street_name", "street_number", "apt", "zip_code", "district", "city", "state"]
    datakey += ["rg", "birth_date", "gender"] if user_type == "physical_person" else ["cnpj", "state_tax_registration", "legal_business_name", "trade_name", "scrap_purchase_authorization"]
    data = {}
    nullAbleValues = ["cellphone2", "photo", "landline", "scrap_purchase_authorization"]

    for requiredData in datakey:
        value = request.form[requiredData]
        if value == "" and requiredData not in nullAbleValues:
            msg = "Complete all the inputs"
            return jsonify({"InputError": msg})
        data[requiredData] = value
        
    #validations
    if not is_email(data["email"]):
        msg = "Invalid email"
        return jsonify({"InputError": msg})
    
    if not is_phone_number(data["cellphone1"]) or ( not is_phone_number(data["cellphone2"]) and data["cellphone2"] != "") or (not is_phone_number(data["landline"]) and data["landline"]!= ""):
        msg = "Invalid chellphone"
        return jsonify({"InputError": msg})
    if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]): #without contractions
        msg = "Invalid location data"
        return jsonify({"InputError": msg})
    
    if user_type == "physical_person":
        if is_cpf(data["cpf"]) and is_rg(data["rg"]):
            if not User_validation(data["username"], data["email"], data["cpf"],rg=data["rg"]):
                msg = "There is already a user with that name, email, CPF or Rg"
                return  jsonify({"InputError": msg})
        else:
            msg = "Invalid CPF"
            return  jsonify({"InputError": msg})
    else:
        if is_cnpj(data["cnpj"]) and state_tax_registration_validation(data["state_tax_registration"], data["state"]):
            if not User_validation(data["username"], data["email"], data["cpf"], cnpj=data["cnpj"]):
                msg = "There is already a user with that name, email or CNPJ"
                return  jsonify({"InputError": msg})
        else:
            msg = "Invalid CNPJ or state_tax_registration"
            return  jsonify({"InputError": msg})
        
    create_user(data)

    
    return jsonify({"redirect":url_for("loginPage.LoginPage")})

