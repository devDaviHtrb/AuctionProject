
from flask import Blueprint, redirect, request, session, url_for, Response, make_response

changeConfig = Blueprint("changeConfig", __name__)

HOUR = 3600
DAY = HOUR*24

#called after the user press the button for save the changes in config page
#the inputs values will be wrote with cookies values
#input ids must have the same name as cookies
@changeConfig.route("/changeConfig", methods=[ "POST"])
def ChangeConfig() -> Response:
    response = make_response(redirect(url_for("configPage.ConfigPage")))
    for cookie in request.form.keys():
        response.set_cookie(cookie, request.form.get(cookie), max_age=3*HOUR) if cookie != "StyleMode" else response.set_cookie(cookie, request.form.get(cookie), max_age=DAY)
    return response