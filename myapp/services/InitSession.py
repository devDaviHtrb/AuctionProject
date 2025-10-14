from flask import session


def init_session(user):
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["admin"] = user.admin
