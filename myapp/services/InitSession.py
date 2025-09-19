from flask import session

def init_session(user:str) -> None:
    session["User"] = user