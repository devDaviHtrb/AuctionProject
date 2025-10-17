from functools import wraps
from flask import Flask, abort, request, session

#from flask_login import current_user

publicRoutes = []
commonRoutes = []
adminRoutes = []



def init_authDecorator(app: Flask) -> None:
    @app.before_request
    def VerifyPermission():
        print(publicRoutes, commonRoutes, adminRoutes)
        if request.endpoint in publicRoutes:
            return
        if not session.get("user_id") and request.endpoint in commonRoutes:
            print(session.get("user_id"))
            abort(401)
            return
        if  session.get("id"):
            if not session.get("admin") == False and request.endpoint in adminRoutes:
                abort(403) 
                return
        
           

