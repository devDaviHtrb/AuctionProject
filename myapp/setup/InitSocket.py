from flask_socketio import SocketIO
from flask import Flask

socketIo = SocketIO()

def init_socket(app: Flask) -> SocketIO:
    socketIo.init_app(app)
    return socketIo