from flask import render_template, Response

def NotFoundPage(error: str) -> Response:
    return render_template("404.html"), 404