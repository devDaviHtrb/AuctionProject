from flask import Flask, render_template, url_for
from flask_login import LoginManager
from typing import Optional, Any

from myapp.models.Users import users

login_manager =  LoginManager()
login_manager.login_view = None


@login_manager.user_loader
def user_loader(usersId: int) -> Optional[Any]:
    return users.query.get(int(usersId))

def init_loginManager(app: Flask) -> None:
    return login_manager.init_app(app)