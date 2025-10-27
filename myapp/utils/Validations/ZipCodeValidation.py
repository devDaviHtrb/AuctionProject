from brazilcep import get_address_from_cep, exceptions
from typing import Optional

def zip_code_validation(zip_code:str) -> Optional[str]:
    try:
        adress = get_address_from_cep(zip_code)
        return adress
    except exceptions.CEPNotFound:
        return