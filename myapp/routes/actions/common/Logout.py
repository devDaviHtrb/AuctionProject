
from flask import Blueprint, redirect, session, url_for, Response, request, make_response
from myapp.utils.LinksUrl import HOME_PAGE, home
from typing import Tuple

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET", "POST"])
def logout() -> Tuple[Response, int]:
    response = make_response("", 302)
    response.headers["Location"] = url_for(HOME_PAGE)
    response.delete_cookie("user_id")
    for key in session.keys():
        session[key] = None
        print(session[key])
    return response