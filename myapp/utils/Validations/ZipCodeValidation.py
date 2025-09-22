from brazilcep import get_address_from_cep, exceptions


def zip_code_validation(zip_code):
    try:
        adress = get_address_from_cep('01001-000')
        return adress
    except exceptions.CEPNotFound:
        return False