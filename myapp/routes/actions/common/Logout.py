
from flask import Blueprint, session, url_for, Response, make_response
from myapp.utils.LinksUrl import HOME_PAGE
from typing import Tuple
from myapp.utils.LinksUrl import HOME_PAGE

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET", "POST"])
def logout() -> Tuple[Response, int]:
    response = make_response("", 302)
    response.headers["Location"] = url_for(HOME_PAGE)
    response.delete_cookie("user_id")
    session.clear()

    return response