from myapp.models.LegalPerson import legal_persons
from myapp.models.User import users


def User_validation(username, email, cpf=None, cnpj=None):
    if users.query.filter_by(username=username).first():
        return False
    if users.query.filter_by(email=email).first():
        return False
    if cpf and users.query.filter_by(CPF=cpf).first():
        return False
    if cnpj and legal_persons.query.filter_by(CNPJ=cnpj).first():
        return False
    return True #Create this user is possible