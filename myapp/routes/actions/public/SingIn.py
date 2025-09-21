from flask import Blueprint, jsonify, redirect, url_for, request, Response

from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons
from myapp.models.User import users

from myapp.utils.utils import get_columns_names, is_cpf, is_cnpj, is_email, User_validation

singIn = Blueprint("singIn", __name__)

@singIn.route("/singIn", methods=["POST"])

def SingIn():
    user_type = request.form["userType"]#legal_person or physical_person


    #required data
    datakey = ["username","password","email","cp","name","userType","cellphone1","cellphone2","photo", "street_name", "street_number", "apt", "zip_code", "district", "city", "state"]
    datakey += ["rg", "birth_date", "gender"] if user_type == "physical_person" else ["cnpj", "state_tax_registration", "legal_business_name", "trade_name", "scrap_purchase_authorization"]
    data = {}

    for requiredData in datakey:
        value = request.form[requiredData]
        if value == "" and requiredData!="cellphone2" or  value == "" and requiredData!="photo":
            msg = "Complete all the inputs"
            return jsonify({"InputError": msg})
        data[requiredData] = value
        
    #validations
    if not is_email(data["email"]):
        msg = "Invalid email"
        return jsonify({"InputError": msg})
    
    if user_type == "physical_person":
        if is_cpf(data["cpf"]):
            if not User_validation(data["username"], data["email"], data["cpf"]):
                msg = "There is already a user with that name, email or CPF"
                return  jsonify({"InputError": msg})
        else:
            msg = "Invalid CPF"
            return  jsonify({"InputError": msg})
    else:
        if is_cnpj(data["cnpj"]):
            if not User_validation(data["username"], data["email"], data["cpf"], data["cnpj"]):
                msg = "There is already a user with that name, email or CNPJ"
                return  jsonify({"InputError": msg})
        else:
            msg = "Invalid CNPJ"
            return  jsonify({"InputError": msg})
        

    
    return jsonify({"redirect":url_for("loginPage.LoginPage")})

