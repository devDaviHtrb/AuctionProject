from flask import Blueprint, Response, url_for, session, request, make_response
from myapp.services.CreateUser import create_user
from myapp.services.InitSession import init_session
from myapp.services.Messages import auth_message
from myapp.utils.AuthPending import *
from myapp.models.Users import users
from werkzeug.security import generate_password_hash
from myapp.services.setCookies import set_cookies
from myapp.utils.LinksUrl import *

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/set/adm")
def setAdm():
    session["user_id"] = 3
    session["admin"] = True
    #if 
    return "", 200

@auth_bp.route("/auth/<string:token>", methods = ["POST", "GET"])
def auth(token:str) -> Response:
    print("auth")
    token_data = get_by_pending(token)

    if (not token_data): #not token
        return sing_in()

    type = token_data.get("type")
    data = token_data.get("user_data")
    
    if(type == "login"):
        user = users.query.get(data.get("user_id"))       
        if (not user):
            return sing_in()
        response = make_response(profile())
        init_session(user) ## <--
        set_cookies(request, response, user_id = user.user_id)
        pop_by_pending(token)
        return response
    
    elif(type == "create"):
       
        user = users.get_by_email(
            data.get("email")
        )
        if (not user):
            create_user(data)

    elif(type == "reset"):
        user = users.get_by_email(
            data.get("email")
        )
        new_password = request.form.get("new_password", None)
        if (not user):
            return sing_in()
        if (not new_password):
            return change(token=token)
        user.set_password(new_password)

    else:
        return sing_in()
    
    pop_by_pending(token)
    return login()

@auth_bp.route("/auth/resend")
@auth_bp.route("/auth/resend/<string:email>")
def resend(email:str = None) -> Response:
    if(not email):
        return sing_in()
    token = get_by_emails_dict(email)
    auth_message(
        email = email,
        content = url_for("auth.auth", token = token)
    )
    if (not token):
        return login()
    return wait_login(email)

@auth_bp.route("/auth/change/<string:email>")
def changePassword(email:str) -> Response:
    token = get_by_emails_dict(email)
    ## get token
    if (not token):
        if(not users.get_by_email(email)): # no have users with this email
            return sing_in()
        #add in token
        token = add_in(
            type = "reset",
            data = {"email": email}
        )
        auth_message(
            email =     email,
            content =   url_for("auth.auth",token=token, _external=True)
        )
        return wait_change(email)

    # if token exists resend email   
    pop_by_pending(token)
    return changePassword(email)

        

