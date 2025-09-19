from flask import Blueprint, jsonify, redirect, url_for, request

from myapp.models.LegalEntity import LegalEntity
from myapp.models.NaturalPerson import NaturalPerson
from myapp.models.User import User

from myapp.utils.utils import get_columns_names, is_cpf, is_cnpj, is_email, User_validation

singIn = Blueprint("singIn", __name__)

@singIn.route("/singIn", methods=["POST"])
def SingIn():
    user_type = request.form["userType"]#company or natural person

    #required data
    datakey = get_columns_names(User)
    datakey += get_columns_names(NaturalPerson) if user_type == "person" else  get_columns_names(LegalEntity)
    data = {}

    for requiredData in datakey:
        value = request.form[requiredData]
        if value == "":
            msg = "Complete all the inputs"
            return jsonify({"InputError": msg})
        data[requiredData] = value
        
    #validations
    if not is_email(data["email"]):
        msg = "Invalid email"
        return jsonify({"InputError": msg})
    
    if user_type == "person":
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