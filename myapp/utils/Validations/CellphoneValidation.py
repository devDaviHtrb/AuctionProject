import phonenumbers
from phonenumbers import is_valid_number, parse


def cellphone_validation(num):
    num =  parse(num, "BR")
    if is_valid_number(num):
        return True
    else:
        return False
