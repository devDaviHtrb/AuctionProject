from flask import Blueprint, render_template

waitingPage = Blueprint("waitingPage", __name__)

@waitingPage.route("/waitingPage")
@waitingPage.route("/waitingPage/<string:user_type>")
@waitingPage.route("/waitingPage/<string:user_type>/<string:link>")
@waitingPage.route("/waitingPage/<string:user_type>/<string:link>/<string:email>")
def WaitingPage(user_type: str = None, link: str = "signUpPage.SignUpPage", email: str = None):
    return render_template("Waiting.html", link=link, email=email, user_type=user_type)
