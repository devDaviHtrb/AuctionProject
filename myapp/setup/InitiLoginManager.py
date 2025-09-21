from flask import Flask, render_template, url_for
from flask_login import LoginManager
from typing import Optional, Any

from myapp.models.User import users

login_manager =  LoginManager()
login_manager.login_view = None

@login_manager.user_loader

def user_loader(userId):
    return users.query.get(int(userId))

def init_loginManager(app: Flask) -> None:
    return login_manager.init_app(app)