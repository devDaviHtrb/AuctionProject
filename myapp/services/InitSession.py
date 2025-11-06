from flask import session
from myapp.models.Users import users
from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons


def init_session(user: users) -> None:
    session["user_photo"] = user.photo if user.photo else "https://res.cloudinary.com/dnet6nodm/image/upload/v1762029407/Users_photos/xlch6finabqgecvcac6r.png"
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["user_wallet"] = user.wallet
    session["admin"] = user.admin_user
    session["email"] = user.email
    session["name"] = user.name
    session["cellphone1"] = user.cellphone1
    session["cellphone2"] = user.cellphone2
    session["landllne"] = user.landline
    l_user = legal_persons.query.filter_by(user_id=user.user_id).first()
    p_user = physical_persons.query.filter_by(user_id=user.user_id).first()
    session["user_type"] = "physical_person" if not l_user else "legal_person"
    if session["user_type"] == "physical_person":
        session["gender"] = p_user.gender
