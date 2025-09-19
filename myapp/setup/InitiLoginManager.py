from flask_login import LoginManager

from myapp.models.User import User

login_manager =  LoginManager()

@login_manager.user_loader
def user_loader(UserId):
    return User.query.get(int(UserId))

def init_loginManager(app):
    return login_manager.init_app(app)