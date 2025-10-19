import myapp.services.Messages as msgs
from flask import Blueprint, jsonify, url_for, request, Response
from myapp.models.Users import users
from myapp.utils.AuthPending import add_in
from myapp.services.CreateUser import create_user
from myapp.utils.Validations.validations import *
from myapp.utils.utils import uploadImage
from typing import Tuple

singIn = Blueprint("singIn", __name__)

@singIn.route("/singIn", methods=["POST"])
def SingIn() -> Tuple[Response, int]:
    user_type = request.form.get("userType", "physical_person")  # legal_person or physical_person


    datakey = [
        "username", "password", "email", "cpf", "name", "userType",
        "cellphone1", "cellphone2", "landline", "photo",
        "street_name", "street_number", "apt", "zip_code",
        "district", "city", "state"
    ]


    nullAbleValues = [
        "cellphone2", "cnpj", "cpf", "rg", "photo", "landline",
        "scrap_purchase_authorization", "cellphone1", "street_name",
        "street_number", "apt", "zip_code", "district", "city",
        "state", "rg", "birth_date", "gender", "state_tax_registration", "legal_business_name", "trade_name", "scrap_purchase_authorization"
    ]

    data = {}
    missingInfo = []

    for requiredData in datakey:
        value = request.form.get(requiredData) if requiredData != "photo" else request.files.get("photo")
        if (value is None or value == "") and requiredData not in nullAbleValues:
            missingInfo.append(requiredData)
        else:
            data[requiredData] = value if value != "" else None

    if missingInfo:
        return jsonify({"InputError": "Complete all the inputs", "MissingInformation": missingInfo}), 400
    if not is_email(data["email"]) :
        print("error")
        return jsonify({"InputError": "Invalid email"}), 400


    for phone in ["cellphone1", "cellphone2", "landline"]:
        if data.get(phone) and not is_phone_number(data[phone]):
            return jsonify({"InputError": f"Invalid {phone}"}), 400

    if all(data.get(key) for key in ["zip_code", "district", "state", "city"]):
        if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]):
            return jsonify({"InputError": "Invalid location data"}), 400
    

    if data.get("photo"):
        if validateImg(data["photo"]):
            photo_url = uploadImage(data["photo"], "Users_photos")
            if photo_url:
                data["photo_url"] = photo_url
            else:
                return jsonify({"InputError": "Image DB connection error"}), 400
        else:
            return jsonify({"InputError": "Invalid file"}), 400

    if user_type == "physical_person":
        if data.get("cpf") and not is_cpf(data["cpf"]):
            return jsonify({"InputError": "Invalid CPF"}), 400
        if data.get("rg") and not is_rg(data["rg"]):
            return jsonify({"InputError": "Invalid RG"}), 400
        if not User_validation(data["username"], data["email"], data["cpf"], rg=data.get("rg")):
            return jsonify({"InputError": "User with same name, email, CPF, or RG exists"}), 400
    else:
        if data.get("cnpj") and not is_cnpj(data["cnpj"]):
            return jsonify({"InputError": "Invalid CNPJ"}), 400
        if not User_validation(data["username"], data["email"], data.get("cpf"), cnpj=data.get("cnpj")):
            return jsonify({"InputError": "User with same name, email, or CNPJ exists"}), 400


    token = add_in(data=data, type="create")


    msgs.auth_message(email=data["email"], content=url_for("auth.auth", token=token, _external=True))


    if "photo" in data:
        del data["photo"]

    return jsonify({"redirect": url_for("waitingPage.WaitingPage"), "Data": data}), 200
