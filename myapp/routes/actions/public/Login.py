from flask import jsonify, Blueprint, request, make_response, url_for, Response

from myapp.models.Users import users
from myapp.services.setCookies import set_cookies
from flask_login import login_user
from typing import Tuple
from werkzeug.security import check_password_hash

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login() -> Tuple[Response, int]:
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        if not name or not password:
            msg = "Fill in all fields"
            return jsonify({"InputError": msg}), 400
        
        user = users.query.filter_by(username=name).first()
        print(user)
        
        if not user or not check_password_hash(user.password, password):
            msg = "This user is wrong or don't exists"
            return jsonify({"InputError": msg}), 400
        
        if not check_password_hash(user.password, password):
            msg = "The password is wrong or don't exists"
            return jsonify({"InputError": msg}), 400
    
        login_user(users.query.filter_by(username=name).first(), remember=True)
        
        response = make_response(jsonify({"redirect":url_for("profile.Profile")})) 
        set_cookies(request, response)
        
        
        return response, 200
        
