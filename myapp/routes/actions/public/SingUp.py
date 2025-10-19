from flask import Blueprint, jsonify, url_for, request, Response
from myapp.models.Users import users
from myapp.utils.AuthPending import add_in
from myapp.services.CreateUser import create_user
from myapp.utils.Validations.Async.As_Email import async_email
from myapp.utils.Validations.Async.As_UploadImage import async_upload_image
from myapp.utils.Validations.validations import *
from typing import Tuple
from threading import Thread

singUp = Blueprint("singUp", __name__)

@singUp.route("/singUp", methods=["POST"])
def SingUp() -> Tuple[Response, int]:
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
        "state", "rg", "birth_date", "gender", "state_tax_registration",
        "legal_business_name", "trade_name", "scrap_purchase_authorization"
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

    if not is_email(data["email"]):
        return jsonify({"InputError": "Invalid email"}), 400

    for phone in ["cellphone1", "cellphone2", "landline"]:
        if data.get(phone) and not is_phone_number(data[phone]):
            return jsonify({"InputError": f"Invalid {phone}"}), 400

    if all(data.get(key) for key in ["zip_code", "district", "state", "city"]):
        if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]):
            return jsonify({"InputError": "Invalid location data"}), 400

    # === CPF / CNPJ validation ===
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

    # === Token ===
    token = add_in(data=data, type="create")

    # === Background Upload (Thread) ===
    if data.get("photo"):
        if validateImg(data["photo"]):
            file = data["photo"]
            folder = "Users_photos"
            Thread(target=async_upload_image, args=(file, data, folder)).start()
        else:
            return jsonify({"InputError": "Invalid file"}), 400

    

    Thread(target=async_email, args=(data["email"], token)).start()

  
    if "photo" in data:
        del data["photo"]

    return jsonify({"redirect": url_for("waitingPage.WaitingPage", user_type=user_type), "Data": data}), 200
