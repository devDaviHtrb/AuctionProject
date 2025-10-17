from flask import Blueprint, render_template

waiting_page_bp = Blueprint("waitingPage", __name__)

@waiting_page_bp.route("/waitingPage")
@waiting_page_bp.route("/waitingPage/<string:link>")
def WaitingPage(link:str = "/singIn"):
    return render_template("Waiting.html", link = link)
