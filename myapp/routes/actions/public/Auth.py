import myapp.services.Messages as msgs
import myapp.repositories.UserRepository as user_repository
from myapp.services.InitSession import init_session
from myapp.services.GoogleAuth import create_flow, get_id_info, get_extra_user_info
from myapp.services.AuthTokens import *
from myapp.models.Users import users
from myapp.services.CookiesService import set_cookies
import myapp.utils.LinksUrl as links
from typing import Tuple
import google.auth.transport.requests
from werkzeug.security import generate_password_hash
from secrets import token_urlsafe
from flask import *
import google.auth._helpers

AUTH_CONFIRM = links.AUTH_CONFIRM

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/google/redirect")
def google_redirect() -> Response:
    flow = create_flow()

    google.auth._helpers.CLOCK_SKEW_SECS = 2

    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/auth/google/validate")
def google_validate() -> Response:
    flow = create_flow()
    flow.fetch_token(authorization_response = request.url)

    if(session.get("state") != request.args.get("state")):
        return redirect(url_for(links.LOGIN_PAGE))
    
    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()

    id_info = get_id_info(
        credentials,
        request_session
    )

    email = id_info.get("email", None)
    if(not email):
        return redirect(url_for(links.SIGN_UP_PAGE))
    
    user = user_repository.get_by_email(email)
    if(user):
        response = redirect(url_for(links.HOME_PAGE))
        init_session(user)
        set_cookies(request, response, user.user_id)
        return response

    name =      id_info.get("name")
    username =  email.split("@")[0]
    password =  generate_password_hash(token_urlsafe(32))

    birth_date, gender = get_extra_user_info(
        credentials
    )
    data ={
        "email":        email,
        "name":         name,
        "username":     username,
        "password":     password,
        "birth_date":   birth_date,
        "gender":       gender
    }

    user = user_repository.save_item(data)
    response = redirect(url_for(links.HOME_PAGE))

    init_session(user)
    set_cookies(request, response, user.user_id)

    msgs.welcome_message(
        email =     email,
        content =   name,
        url =      url_for(links.AUTH_RESEND, email = email, _external=True)
    )
    return response

@auth_bp.route("/auth/confirm/<string:token>", methods = ["POST", "GET"])
def auth(token:str) -> Tuple[Response, int]:
    token_data = get_by_pending(token)

    if (not token_data): #not token
        return redirect(url_for(links.SIGN_UP_PAGE))

    type = token_data.get("type")
    data = token_data.get("user_data")
    
    if(type == "login"):
        user = users.query.get(data.get("user_id"))       
        if (not user):
            return redirect(url_for(links.SIGN_UP_PAGE))

        response =  redirect(url_for(links.HOME_PAGE))
        init_session(user) ## <--
        set_cookies(request, response, user_id = user.user_id)
        pop_by_pending(token)
        return response
    
    elif(type == "create"):
       
        user = user_repository.get_by_email(
            data.get("email")
        )
        if (not user):
            user_repository.save_item(data)
        
        pop_by_pending(token)
        return redirect(url_for(links.HOME_PAGE))

    elif(type == "reset"):
        user = user_repository.get_by_email(
            data.get("email")
        )
        new_password = request.form.get("new_password", None)
        if (not user):
            return redirect(url_for(links.SIGN_UP_PAGE))
        if (not new_password):
            return redirect(url_for(
                links.CHANGE_PASSWORD_PAGE,
                token = token
            ))
        user_repository.set_password(user,new_password)

    else:
        return links.sign_up()
    
    pop_by_pending(token)
    return links.login()

@auth_bp.route("/auth/resend")
@auth_bp.route("/auth/resend/<string:email>")
def resend(email:str = None) -> Tuple[Response, int]:
    if(not email):
        return redirect(url_for(links.SIGN_UP_PAGE))
    token = get_by_emails_dict(email)
    msgs.auth_message(
        email = email,
        content = url_for(AUTH_CONFIRM, token = token)
    )
    if (not token):
        return redirect(url_for(links.LOGIN_PAGE))
    return redirect(url_for(
        links.WAITING_PAGE,
        email = email
    ))

@auth_bp.route("/auth/change", methods = ["POST"])
def change_password() -> Response:
    email = request.form.get("email", None)

    if(not email or not user_repository.get_by_email(email)): # no have users with this email
        return redirect(url_for(links.SIGN_UP_PAGE))
    #add in token
    token = add_token(
        type = "reset",
        data = {"email": email}
    )
    msgs.auth_message(
        email =     email,
        content =   url_for(AUTH_CONFIRM,token=token, _external=True)
    )
    return redirect(url_for(
        links.WAITING_PAGE,
        email = email
    )) 


        

