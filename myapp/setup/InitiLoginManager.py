from flask import render_template, url_for
from flask_login import LoginManager

from myapp.models.User import users

login_manager =  LoginManager()
login_manager.login_view = None

@login_manager.user_loader
def user_loader(userId):
    return users.query.get(int(userId))

def init_loginManager(app):
    return login_manager.init_app(app)