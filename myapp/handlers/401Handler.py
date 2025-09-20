from flask import render_template, Response

def NotUser(error: str) -> Response:
    return render_template("401.html"), 401