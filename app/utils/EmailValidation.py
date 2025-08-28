from email_validator import EmailNotValidError, validate_email


def validateEmail(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False
        