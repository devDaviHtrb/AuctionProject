from flask import redirect, render_template, Blueprint, request, make_response, url_for

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST", "GET"])
def Login():
    msg = ""
    
    if request.method == "POST":
        print("Requisiion submited")
        name = request.form["username"]
        password = request.form["password"]
        if name == None or password == None:
            msg = "Fill in all fields"
            return render_template("Login.html", message = msg)
        #awaiting the DB creation
        #if username and password in DB:
        response = make_response(redirect(url_for("profile.Profile")))
        response.set_cookie("User", name)
        return response
        
    return render_template("Login.html", message = msg)