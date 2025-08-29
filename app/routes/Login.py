from flask import redirect, render_template, Blueprint, request, make_response, url_for

from app.services.InitSession import init_session

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login():
    msg = ""
    
    if request.method == "POST":
        print("Requisition submitted")
        name = request.form["username"]
        password = request.form["password"]
        if not name or not password:
            msg = "Fill in all fields"
            return render_template("Login.html", message = msg)
        #awaiting the DB creation
        #if username and password in DB:
        response = make_response(redirect(url_for("profile.Profile")))
        
        init_session(name)
        if request.cookies.get("StyleMode") == None:
            response.set_cookie("StyleMode", "light")
        return response
        
    return render_template("Login.html", message = msg)