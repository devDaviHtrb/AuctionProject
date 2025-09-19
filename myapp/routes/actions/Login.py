from flask import jsonify, redirect, render_template, Blueprint, request, make_response, url_for

from myapp.models.User import User
from myapp.services.setCookies import set_cookies
from flask_login import login_user
from werkzeug.security import check_password_hash
from myapp.setup.InitSqlAlchemy import db
login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        if not name or not password:
            msg = "Fill in all fields"
            return jsonify({"InputError": msg})
        
        user = User.query.filter_by(username=name).first()
        print(user.password)
        if not user or check_password_hash(user.password, password):
            msg = "The username or password is  wrong or don't exists"
            return jsonify({"InputError": msg})
        
        login_user(user, remember=True)
        
        response = make_response(jsonify({"redirect":url_for("profile.Profile")})) 
        set_cookies(request, response)
        
        return response
        
