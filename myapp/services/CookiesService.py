from flask import Request, Response
from config import Config
from cryptography.fernet import Fernet

FERNET_KEY = Config.FERNET_KEY
fernet = Fernet(FERNET_KEY)

HOUR = 3600
DAY = HOUR*24
COOKIES_DEFAULT = {"StyleMode":{"value":"light", "max_age":DAY},"AccessibilityMode":{"value":"off", "max_age":DAY}, "AnonymousMode":{"value":"off", "max_age":HOUR*3} }

def set_cookies(request: Request, response: Response, user_id:int = None) -> None:
    if user_id:
        token = fernet.encrypt(str(user_id).encode())
        response.set_cookie(
            "user_id",
            token.decode(),
            httponly=True,   
            secure=False,  #The flask doesn't save cookies if secure==False and the server is localhost, so secure will be True on apresentation day  
            samesite="Lax",  
            max_age=HOUR * 3   
        )
    for key in COOKIES_DEFAULT.keys():
        if not request.cookies.get(key, None):
            response.set_cookie(key, COOKIES_DEFAULT[key]["value"], max_age=COOKIES_DEFAULT[key]["max_age"])
   
    