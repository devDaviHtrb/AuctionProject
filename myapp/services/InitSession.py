from flask import session

def init_session(user):
    session["User"] = user