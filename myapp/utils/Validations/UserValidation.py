from myapp.models.LegalEntity import LegalEntity
from myapp.models.User import User


def User_validation(username, email, cpf=None, cnpj=None):
    if User.query.filter_by(username=username).first():
        return False
    if User.query.filter_by(email=email).first():
        return False
    if cpf and User.query.filter_by(CPF=cpf).first():
        return False
    if cnpj and LegalEntity.query.filter_by(CNPJ=cnpj).first():
        return False
    return True #Create this user is possible