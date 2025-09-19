from functools import wraps
from flask import abort, current_app, request
from flask_login import current_user

publicRoutes = []
communRoutes = []
adminRoutes = []

def init_authDecorator(app):
    @app.before_request
    def VerifyPermission():
        print(publicRoutes, communRoutes, adminRoutes)
        if request.endpoint in publicRoutes:
            return
        elif not current_user.is_authenticated and request.endpoint in communRoutes:
            abort(401)
            #adicionar o login reuqired
        elif not current_user.admin and request.endpoint in adminRoutes:
            abort(403) 
        
           

