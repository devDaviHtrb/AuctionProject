from PYBRDOC import Cnpj

def CNPJ_validation(cnpj:str) -> bool:
    return Cnpj(cnpj).isValid #Without mask