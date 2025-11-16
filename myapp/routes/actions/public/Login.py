from flask import jsonify, Blueprint, request, url_for, Response
import myapp.repositories.UserRepository as user_repository
from myapp.services.AuthTokens import add_token
from myapp.services.Messages import auth_message
from myapp.services.InitSession import init_session
from myapp.services.CookiesService import set_cookies
from myapp.utils.LinksUrl import profile, AUTH_CONFIRM, AUTH_RESEND
import myapp.repositories.UserRepository as user_repository
from typing import Tuple
from werkzeug.security import check_password_hash
from datetime import datetime

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST", "GET"])
def login() -> Tuple[Response, int]:
    if request.method == "POST":

        name =      request.form["username"]
        password =  request.form["password"]

        if not name or not password:
            msg = "Fill in all fields"
            return jsonify({"InputError": msg}), 400
        
        user = user_repository.get_by_username(name)
        if(not user):
            user = user_repository.get_by_email(name)
        
        if not user or not check_password_hash(user.password, password):
            msg = "This user is wrong or don't exists"
            return jsonify({"InputError": msg}), 400
        
        data = {
            "user_id":          user.user_id,
            "email":            user.email,
            "username":         user.username,
            "login_datetime":   datetime.now()
        }
        
        if(user_repository.get_two_factor_auth(user)):
            token = add_token(
                data=   data,
                type=   "login"
            )
            auth_message(
                email =     user.email,
                content =   url_for( AUTH_CONFIRM, token = token, _external = True)
            )
            return jsonify({
                "redirect":url_for(
                        AUTH_CONFIRM,
                    link = AUTH_RESEND,
                    email = user.email
                ),
                "Data":data
            }), 200

        init_session(user)
        response = profile() #json
        set_cookies(request, response, user_id = user.user_id)

        return response, 200
        
