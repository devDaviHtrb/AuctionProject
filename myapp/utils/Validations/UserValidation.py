from myapp.models.Users import users
from myapp.models.PhysicalPerson import physical_persons
from myapp.models.LegalPerson import legal_persons
from sqlalchemy import or_

def User_validation(
    username:str,
    email:str = None,
    cpf:str =   None,
    rg:str =    None,
    cnpj:str =  None
) -> bool:
    filters = [users.username == username, users.email == email] if email else [users.username == username]

    if cpf:
        filters.append(users.cpf == cpf)


    user = users.query.filter(or_(*filters)).first()
    existing_pp = physical_persons.query.filter_by(rg=rg).first()  if rg else None
    existing_lp = legal_persons.query.filter_by(cnpj=cnpj).first()  if cnpj else None

    if user or existing_lp or existing_pp:
        print(user.name)
        return False
    else:
        return True
