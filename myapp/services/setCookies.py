from flask import Request, Response

def set_cookies(request: Request, response: Response) -> None:
    if not request.cookies.get("StyleMode"):
        response.set_cookie("StyleMode", "light")

