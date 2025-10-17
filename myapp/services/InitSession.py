from flask import session
#from myapp.
from myapp.models.Users import users


def init_session(user: users) -> None:
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["admin"] = user.admin_user
