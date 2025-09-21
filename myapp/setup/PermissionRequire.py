from functools import wraps
from flask import Flask, abort, current_app, request
#from flask_login import current_user

publicRoutes = []
commonRoutes = []
adminRoutes = []

current_user = True

def init_authDecorator(app: Flask) -> None:
    @app.before_request
    def VerifyPermission():
        print(publicRoutes, commonRoutes, adminRoutes)
        if request.endpoint in publicRoutes:
            return
        elif not current_user and request.endpoint in commonRoutes:
            abort(401)
        elif not current_user.admin_user and request.endpoint in adminRoutes:
            abort(403) 
        
           

