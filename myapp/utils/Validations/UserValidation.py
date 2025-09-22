from myapp.models.LegalPerson import legal_persons
from myapp.models.Users import users


def User_validation(username:str, email:str, cpf:str=None, cnpj:str=None, rg=None) -> bool:
    if users.query.filter_by(usersname=username).first():
        return False
    if users.query.filter_by(email=email).first():
        return False
    if cpf and users.query.filter_by(CPF=cpf).first():
        return False
    if users.query.filter_by(rg=rg).first():
        return False
    if cnpj and legal_persons.query.filter_by(CNPJ=cnpj).first():
        return False
    return True #Create this user is possible