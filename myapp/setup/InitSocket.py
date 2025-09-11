from flask_socketio import SocketIO
from flask import Flask

socket_io = SocketIO()

def init_socket(app: Flask) -> SocketIO:
    socket_io.init_app(app)
    return socket_io