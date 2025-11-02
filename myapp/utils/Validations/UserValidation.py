from myapp.models.Users import users
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
    if rg:
        filters.append(users.rg == rg)
    if cnpj:
        filters.append(users.cnpj == cnpj)

    existing_user = users.query.filter(or_(*filters)).first()
    return not existing_user 