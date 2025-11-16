from PYBRDOC import InscricaoEstadual as IE
def state_tax_registration_validation(STR:str, uf:str) -> bool:
    return IE(STR, siglaUF=uf).isValid

