from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = "loginPage.LoginPage"

def init_LoginManager(app):
    login_manager.init_app(app)
    return login_manager