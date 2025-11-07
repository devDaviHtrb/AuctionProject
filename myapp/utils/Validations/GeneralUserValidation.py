from myapp.utils.Unmask import unmask
from myapp.utils.Validations.validations import *
from flask import Request
from myapp.utils.GetMissingInfo import get_missing_info
from myapp.utils.utils import upload_image
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
    'state_tax_registration', 'legal_business_name', 'trade_name'
]

def set_type(user_type:str) -> None:
     global datakey
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

def general_validation(request:Request) -> Tuple[Dict[str, Any], int]:
    user_type = request.form.get("userType", "physical_person")
    set_type(user_type)
    data, code = get_missing_info(
        request,
        datakey,
        nullAbleValues
    )
    if (code != 200):
         return data, code
    
    if not is_email(data["email"]):
        return {
             "Type":    "InputError",
             "content": "Invalid email"
        }, 400
    
    for phone in ["cellphone1", "cellphone2", "landline"]:
        if data.get(phone, None):
            data[phone] = unmask(data[phone])
            if not is_phone_number(data[phone]):
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
    
    
    if user_type == "physical_person":
            cpf = data.get("cpf", None)
            rg = data.get("rg", None)

            if cpf:
                cpf = unmask(cpf)
                if not is_cpf(data["cpf"]):
                      return  {
                         "Type":    "InputError",
                         "content": "Invalid CPF"
                    }, 400
                
            if rg:
                rg = unmask(rg)
                if not is_rg(data["rg"]):
                      return  {
                         "Type":    "InputError",
                         "content": "Invalid Rg"
                    }, 400
            
            if not User_validation(data["username"], data["email"], cpf=cpf,rg=rg):
                        return {
                             "Type":    "InputError",
                             "content": "There is already a user with that name, email, CPF or Rg"
                        }, 400
    elif user_type=="legal_person":
        cnpj = unmask(data.get("cnpj", None))
        if not is_cnpj(cnpj):
                      return  {
                         "Type":    "InputError",
                         "content": "Invalid Rg"
                    }, 400
        
        if not state_tax_registration_validation(data["state_tax_registration"], data["state"]):
            return {
                 "Type":    "InputError",
                 "content": "Invalid CNPJ or state_tax_registration"
            }, 400
        
        if not User_validation(data["username"], data["email"], cpf=cpf, cnpj=cnpj):
                return {
                     "Type":    "InputError",
                     "content": "There is already a user with that name, email, cpf or cnpj"
                }, 400
    return {
         "Type":    "Valid",
         "content": "All information is valid",
         "data":    data
    }, 200