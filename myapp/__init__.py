from flask import Flask
from flask_socketio import SocketIO
from myapp.setup.InitSocket import init_socket
from config import Config


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    #Socket initialization
    socketIo = init_socket(app) 
    
    #Listing blueprints
    from myapp.setup.registerRoutes import register_routes
    register_routes(app)

    import myapp.sockets.Connect

    #Returning instance
    return app, socketIo


