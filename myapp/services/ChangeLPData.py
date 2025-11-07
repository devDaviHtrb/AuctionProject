from flask import redirect, session, url_for
from myapp.models.LegalPerson import legal_persons
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Unmask import unmask
from myapp.utils.Validations.UserValidation import User_validation
from myapp.utils.Validations.validations import is_cnpj


def change_lp_data(request, current_user):
    legal_person=  legal_persons.query.filter_by(user_id=current_user.user_id).first()
    cnpj = request.form.get("cnpj", None)
    trade_name = request.form.get("trade_name", None)
    legal_business_name = request.form.get("legal_business_name", None)
    state_tax_registration =  request.form.get("state_tax_registration", None)
    
    state_tax_registration = unmask(state_tax_registration) if state_tax_registration else state_tax_registration
    cnpj = unmask(cnpj) if cnpj else cnpj

    if is_cnpj(cnpj):
        return redirect(url_for(CONFIG_PAGE, msg="Invalid Rg"))
    if not User_validation(cnpj=cnpj, trade_name=trade_name if session.get("trade_name") else None, state_tax_registration= state_tax_registration if session.get("state_tax_registration") else None, legal_business_name=legal_business_name if session.get("legal_business_name") else None):
        return redirect(url_for(CONFIG_PAGE, msg="There are an user with this trade name, cnpj, state tax registration or legal business name"))
    
    legal_person.cnpj = cnpj if cnpj else legal_person.cnpj
    legal_person.trade_name = trade_name
    legal_person.legal_business_name = legal_business_name
    legal_person.state_tax_registration = state_tax_registration
    session["cnpj"] = cnpj if cnpj else session["cnpj"]
    session["trade_name"] = trade_name
    session["legal_business_name"] = legal_business_name
    session["state_tax_registration"] = state_tax_registration if state_tax_registration else session["state_tax_registration"]