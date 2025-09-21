from flask import session

def init_session(user:str) -> None:
    session["user"] = user