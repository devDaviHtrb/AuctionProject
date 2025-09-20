from validate_docbr import CNPJ

def CNPJ_validation(cnpj:str) -> bool:
    return CNPJ().validate(cnpj) #Without mask