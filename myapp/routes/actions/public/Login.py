from flask import jsonify, Blueprint, request, make_response, url_for, Response
from myapp.utils.LinksUrl import wait_login
from myapp.utils.AuthPending import add_in
from myapp.models.Users import users
from myapp.services.Messages import auth_message
from myapp.services.InitSession import init_session
from myapp.services.setCookies import set_cookies

from typing import Tuple
from werkzeug.security import check_password_hash

from datetime import datetime

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login() -> Tuple[Response, int]:
    print("dsjfsdkjfhkds")
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        if not name or not password:
            msg = "Fill in all fields"
            return jsonify({"InputError": msg}), 400
        
        user = users.query.filter_by(username=name).first()
        
        if not user or not check_password_hash(user.password, password):
            msg = "This user is wrong or don't exists"
            return jsonify({"InputError": msg}), 400
        
        data = {
            "user_id":          user.user_id,
            "email":            user.email,
            "username":         user.username,
            "login_datetime":   datetime.now()
        }
        
        if(user.get_two_factor_auth()):
            token = add_in(data)
            auth_message(
                email =user.email,
                content = url_for("auth.auth",type = "login" ,token = token, _external = True)
            )
            return jsonify({
                "redirect":url_for(
                    "waitingPage.WaitingPage",
                    link = wait_login(user.email)
                ),
                "Data":data
            }), 200

        init_session(user)
        print("sessao iniciada")
        
        response = make_response(jsonify({"redirect":url_for("profile.Profile"), "Data":data})) 
        set_cookies(request, response)

        
        return response, 200
        
