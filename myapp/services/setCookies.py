
def set_cookies(request, response):
    if not request.cookies.get("StyleMode"):
        response.set_cookie("StyleMode", "light")

