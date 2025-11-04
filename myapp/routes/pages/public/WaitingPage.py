from flask import Blueprint, render_template

waitingPage = Blueprint("waitingPage", __name__)

@waitingPage.route("/waitingPage")
@waitingPage.route("/waitingPage/<string:link>")
@waitingPage.route("/waitingPage/<string:link>/<string:email>")
def WaitingPage(link: str = "signUpPage.SignUpPage", email: str = None):
    return render_template("Waiting.html", link=link, email=email)
