from myapp.models.Users import users
from myapp.models.PhysicalPerson import physical_persons
from myapp.models.LegalPerson import legal_persons
from sqlalchemy import or_

def User_validation(
    username:str= None,
    email:str = None,
    cpf:str =   None,
    rg:str =    None,
    cnpj:str =  None,
    trade_name:str = None, 
    legal_business_name:str = None, 
    state_tax_registration:str = None
) -> bool:
    filters = [users.username == username, users.email == email] if email else [users.username == username]

    if cpf:
        filters.append(users.cpf == cpf)

    user = users.query.filter(or_(*filters)).first()

    existing_pp = physical_persons.query.filter_by(rg=rg).first() if rg else None

    filters_lp = []
    if cnpj:
        filters_lp.append(legal_persons.cnpj == cnpj)
    if trade_name:
        filters_lp.append(legal_persons.trade_name == trade_name)
    if legal_business_name:
        filters_lp.append(legal_persons.legal_business_name == legal_business_name)
    if state_tax_registration:
        filters_lp.append(legal_persons.state_tax_registration == state_tax_registration)

    existing_lp = legal_persons.query.filter(or_(*filters_lp)).first() if filters_lp else None

    if user or existing_lp or existing_pp:

        return False
    else:
        return True
