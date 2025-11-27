from flask import redirect, session, url_for
from myapp.models.PhysicalPerson import physical_persons
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Unmask import unmask
from myapp.utils.Validations.UserValidation import User_validation
from myapp.utils.Validations.validations import is_rg
import myapp.repositories.PhysicalPersonRepository as physical_person_repository

def change_pp_data(request, current_user):
    physical_person =   physical_person_repository.get_by_id(current_user.user_id)
    gender =            request.form["gender"]
    rg =                request.form.get("rg", None)
    
    if rg:
        rg = unmask(rg)
        if not is_rg(rg):
            return redirect(url_for(CONFIG_PAGE, msg="Invalid Rg"))
        if not User_validation(rg=rg):
            return redirect(url_for(CONFIG_PAGE, msg="There are an user with this rg"))
        else:
            physical_person.rg = rg
            session["rg"] = rg
            
    physical_person.gender = gender
    session["gender"] = gender
    print(f"{gender}, {physical_person.gender}, {session["gender"]}",flush=True)