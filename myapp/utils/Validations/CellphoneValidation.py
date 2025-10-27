from phonenumbers import PhoneNumber
from phonenumbers import is_valid_number, parse

def cellphone_validation(num:PhoneNumber) -> bool:
    num =  parse(num, "BR")
    if is_valid_number(num):
        return True
    else:
        return False
