from PYBRDOC import CPF

def CPF_validation(cpf:str) -> bool:
    return CPF(cpf).isValid #Without mask