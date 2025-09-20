from flask import render_template, Response

def NotAdmin(error: str) -> Response:
    return render_template("403.html"), 403