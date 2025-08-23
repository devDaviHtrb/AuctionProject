def register_routes(app):
    from app.routes.Home import home
    app.register_blueprint(home)