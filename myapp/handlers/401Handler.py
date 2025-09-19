from flask import render_template

def NotUser(error):
    return render_template("401.html"), 401