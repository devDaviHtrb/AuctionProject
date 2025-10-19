from myapp.models.LegalPerson import legal_persons
from myapp.models.Users import users


from sqlalchemy import or_

def User_validation(username, email, cpf=None, rg=None, cnpj=None):
    filters = [users.username == username, users.email == email]

    if cpf:
        filters.append(users.cpf == cpf)
    if rg:
        filters.append(users.rg == rg)
    if cnpj:
        filters.append(users.cnpj == cnpj)

    existing_user = users.query.filter(or_(*filters)).first()
    return not existing_user 