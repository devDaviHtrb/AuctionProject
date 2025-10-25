
from flask import Blueprint, redirect, session, url_for, Response
from myapp.utils.LinksUrl import home
from typing import Tuple

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET", "POST"])
def logout() -> Tuple[Response, int]:
    session["id"] = None
    session["username"] = None
    session["admin"] = None
    return home(), 200