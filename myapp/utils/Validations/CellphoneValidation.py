from phonenumbers import PhoneNumber
from phonenumbers import is_valid_number, parse
import phonenumbers

def cellphone_validation(num:PhoneNumber) -> bool:
    
    try:
        num =  parse(num, "BR")
        valid = is_valid_number(num)
        return True
    except Exception:
        return False
