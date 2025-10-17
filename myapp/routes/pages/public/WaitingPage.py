from flask import Blueprint, render_template

waiting_page_bp = Blueprint("waitingPage", __name__)

@waiting_page_bp.route("/waitingPage")
@waiting_page_bp.route("/waitingPage/<string:link>")
@waiting_page_bp.route("/waitingPage/<string:link>/<string:email>")
def WaitingPage(link:str = "singInPage.SingInPage", email:str = None):
    return render_template("Waiting.html", link = link, email = email)
