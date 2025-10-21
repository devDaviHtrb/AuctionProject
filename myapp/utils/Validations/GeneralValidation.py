from myapp.utils.Validations.validations import *
from flask import Request
from myapp.utils.utils import uploadImage
from typing import Dict, Any, Tuple

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
    "state",
    "rg",
    "birth_date",
    "gender"
]

def get_missing_info(user_type:str, request:Request) -> Tuple[Dict[str, Any], int]:
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
        if (value == "" or value is None) and requiredData not in nullAbleValues:
            missingInfo.append(requiredData)
            print(missingInfo)
        else:
            data[requiredData] = value

    if missingInfo:
        return {
             "Type":                "InputError",
             "content":             "Complete all the inputs",
             "MissingInformation":  missingInfo
        }, 400
    return data, 200

def general_validation(request:Request) -> Tuple[Dict[str, Any], int]:
    user_type = request.form.get("userType", "physical_person")
    data, code = get_missing_info(user_type, request)
    if (code != 200):
         return data, code
    
    if not is_email(data["email"]):
        return {
             "Type":    "InputError",
             "content": "Invalid email"
        }, 400
    
    if data.get("cellphone1", None):
        if not is_phone_number(data["cellphone1"]) or ( not is_phone_number(data["cellphone2"]) and data["cellphone2"] != "") or (not is_phone_number(data["landline"]) and data["landline"]!= ""):
            return {
                 "Type":    "InputError",
                 "content": "Invalid chellphone"
            }, 400
        
    if data.get("zip_code", None) and data.get("district", None) and data.get("state", None) and data.get("city", None):
        if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]): #without contractions
            return {
                 "Type":    "InputError",
                 "content": "Invalid location data"
            }, 400
    
    if data.get("photo"):
        if validateImg(data["photo"]):
            photo_url = uploadImage(data["photo"], "Users_photos")
            if not photo_url:
                msg = "Image db connection error, sorry, try the submit without img"
                print("Db connection error")
            else: data["photo_url"] = photo_url
        else:
            return {
                 "Type":    "InputError",
                 "content": "Invalid file"
            }, 400

    
    if user_type == "physical_person":
            if data.get("cpf", None) and data.get("rg", None):
                if is_cpf(data["cpf"]) and is_rg(data["rg"]):
                    if not User_validation(data["username"], data["email"], data["cpf"],rg=data["rg"]):
                        return {
                             "Type":    "InputError",
                             "content": "There is already a user with that name, email, CPF or Rg"
                        }, 400
                else:
                    return  {
                         "Type":    "InputError",
                         "content": "Invalid CPF"
                    }, 400
            if not User_validation(data["username"], data["email"]):
                        return  {
                             "Type":    "InputError",
                             "content": "There is already a user with that name, email"
                        }, 400
                       
    elif data.get("cnpj", None):
        if is_cnpj(data["cnpj"]) and state_tax_registration_validation(data["state_tax_registration"], data["state"]):
            if not User_validation(data["username"], data["email"], data["cpf"], cnpj=data["cnpj"]):
                return {
                     "Type":    "InputError",
                     "content": "There is already a user with that name, email or CNPJ"
                }, 400
        else:
            return {
                 "Type":    "InputError",
                 "content": "Invalid CNPJ or state_tax_registration"
            }, 400
        if not User_validation(data["username"], data["email"], data["cpf"], cnpj=data["cnpj"]):
                return {
                     "Type":    "InputError",
                     "content": "There is already a user with that name, email"
                }, 400
    return {
         "Type":    "Valid",
         "content": "All information is valid",
         "data":    data
    }, 303