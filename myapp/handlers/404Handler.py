from flask import render_template

def NotFoundPage(error):
    return render_template("404.html"), 404