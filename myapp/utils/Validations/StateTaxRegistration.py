from PYBRDOC import InscricaoEstadual as IE
from PYBRDOC import ValidadorInscricaoEstadual

def state_tax_registration_validation(STR, uf):
    return ValidadorInscricaoEstadual(IE(STR), uf)