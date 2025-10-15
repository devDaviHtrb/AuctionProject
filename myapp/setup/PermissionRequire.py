from functools import wraps
from flask import Flask, abort, request
from flask_login import current_user
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
        if not current_user.is_authenticated and request.endpoint in commonRoutes:
            
            abort(401)
            return
        if  current_user.is_authenticated:
            if not current_user.admin_user and request.endpoint in adminRoutes:
                abort(403) 
                return
        
           

