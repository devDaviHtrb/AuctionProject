import re
from email_validator import EmailNotValidError, validate_email


def validateEmail(email: str) -> bool:
    email = re.sub(r'[\u200b-\u200d\u2060\xa0]', '', email).strip()

    try:
        valid = validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        print( EmailNotValidError)
        return False
        