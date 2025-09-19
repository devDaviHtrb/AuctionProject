from flask import render_template

def NotAdmin(error):
   
    return render_template("403.html"), 403