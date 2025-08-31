from flask import Blueprint, request, url_for, redirect, make_response

styleMode = Blueprint("styleMode", __name__)


@styleMode.route("/styleMode")
def StyleMode():
    response = make_response(redirect(url_for("profile.Profile")))
    if request.cookies.get("StyleMode") == "light":
        response.set_cookie("StyleMode", "dark")
    else:
        response.set_cookie("StyleMode", "light")
        
    print( request.cookies.get("StyleMode"))

    return response