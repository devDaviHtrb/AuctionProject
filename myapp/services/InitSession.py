from flask import session
from myapp.models.Users import users
import myapp.repositories.PhysicalPersonRepository as physical_person_repository

DEFAULT_IMAGE = "https://res.cloudinary.com/dnet6nodm/image/upload/v1762029407/Users_photos/xlch6finabqgecvcac6r.png"

def init_session(user: users) -> None:
    session["user_photo"] =     user.photo if user.photo else DEFAULT_IMAGE
    session["user_id"] =        user.user_id
    session["username"] =       user.username
    session["user_wallet"] =    user.wallet
    session["admin"] =          user.admin_user
    session["email"] =          user.email
    session["name"] =           user.name
    session["cellphone1"] =     user.cellphone1
    session["cellphone2"] =     user.cellphone2
    session["landllne"] =       user.landline

    p_user = physical_person_repository.get_by_id(user.user_id)
    session["user_type"] = "physical_person" if p_user else "legal_person"

    if session["user_type"] == "physical_person":
        session["gender"] = p_user.gender
