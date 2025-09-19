from validate_docbr import CNPJ

def CNPJ_validation(cnpj):
    return CNPJ().validate(cnpj) #Without mask