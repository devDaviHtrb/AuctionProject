from myapp.extensions import *
from myapp.services.ProductService import restart_closes, restart_open
from flask import Flask
from flask_socketio import SocketIO

def init_extensions(app: Flask) -> SocketIO:

    db = init_db(app)

    create_tables(app, db)

    init_cache(app)

    socket_io = init_socket(app)
    create_SocketEvents()

    init_authDecorator(app)

    register_routes(app)
    register_handlers(app)

    with app.app_context():
        restart_open()
        restart_closes()

    return socket_io
