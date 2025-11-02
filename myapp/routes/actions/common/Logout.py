
from flask import Blueprint, redirect, session, url_for, Response
from myapp.utils.LinksUrl import HOME_PAGE, home
from typing import Tuple

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET", "POST"])
def logout() -> Tuple[Response, int]:
    for key in session.keys():
        session[key] = None
        print(session[key])
    return redirect(url_for(HOME_PAGE)), 200