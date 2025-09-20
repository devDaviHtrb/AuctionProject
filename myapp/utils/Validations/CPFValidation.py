from validate_docbr import CPF

def CPF_validation(cpf:str) -> bool:
    return CPF().validate(cpf) #Without mask