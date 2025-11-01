from functools import wraps
from flask import Flask, request, session, abort, redirect, url_for
from myapp.models.Users import users
from myapp.services.InitSession import init_session
from myapp.services.CookiesService import fernet
from myapp.utils.LinksUrl import LOGIN_PAGE

publicRoutes = []
commonRoutes = []
adminRoutes = []

def init_authDecorator(app: Flask) -> None:
    @app.before_request
    def verify_permission():
        endpoint = request.endpoint
        # public routes
        if endpoint in publicRoutes:
            return

        user_id = session.get("user_id", None)
        if not user_id:
            cookie_user_id = request.cookies.get("user_id")
            if cookie_user_id:
                try:
                    user_id = int(fernet.decrypt(cookie_user_id.encode()))
                    user = users.query.get(user_id)
                    if user:
                        init_session(user)
                    else:
                        user_id = None
                except:
                    user_id = None

        if endpoint in commonRoutes:
            if user_id:
                return
            return redirect(url_for(LOGIN_PAGE))

        if endpoint in adminRoutes:
            if not user_id:
                abort(403)
            if not user or not session.get("admin", None):
                abort(403)  
            return
