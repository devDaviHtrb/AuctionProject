from PYBRDOC import InscricaoEstadual as IE
from PYBRDOC import ValidadorInscricaoEstadual

def state_tax_registration_validation(STR:str, uf:str) -> bool:
    return ValidadorInscricaoEstadual(IE(STR), uf)