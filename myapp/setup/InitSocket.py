from flask_socketio import SocketIO


socketIo = SocketIO()

def init_socket(app):
    socketIo.init_app(app)
    return socketIo