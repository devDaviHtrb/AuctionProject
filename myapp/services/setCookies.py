from flask import Request, Response
from config import Config
from cryptography.fernet import Fernet

FERNET_KEY = Config.FERNET_KEY
fernet = Fernet(FERNET_KEY)

HOUR = 3600
DAY = HOUR*24

def set_cookies(request: Request, response: Response, user_id:int = None) -> None:
    if user_id:
        token = fernet.encrypt(str(user_id).encode())
        response.set_cookie(
            "user_id",
            token.decode(),
            httponly=True,   
            secure=True,     
            samesite="Lax",  
            max_age=HOUR * 3   
        )
    if not request.cookies.get("StyleMode", None):
        response.set_cookie("StyleMode", "light")