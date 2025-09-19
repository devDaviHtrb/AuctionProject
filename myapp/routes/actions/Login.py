from flask import redirect, render_template, Blueprint, request, make_response, url_for
from flask import Response

from typing import Union

from myapp.services.InitSession import init_session
from myapp.services.setCookies import set_cookies

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login() -> Union[Response, str]:
    
    msg = "asdasa"

    if request.method == "POST":
        
        name = request.form["username"]
        password = request.form["password"]

        if not name or not password:
            msg = "Fill in all fields"
            return render_template("Login.html", message = msg)
        
        #awaiting the DB creation
        #if username and password in DB:
        response = make_response(redirect(url_for("profile.Profile")))
        
        init_session(name)
        set_cookies(request, response)
        
        return response
        
    return redirect(url_for("loginPage.LoginPage", msg=msg))