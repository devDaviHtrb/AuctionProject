from flask import Flask
from flask_socketio import SocketIO
from config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    socketIo = SocketIO(app)  
    
    #Listing blueprints
    from app.setup.registerRoutes import register_routes
    register_routes(app)

    #Importing sockets events
    from app import sockets

    #Returning instance
    return {"app":app, "socket":socketIo}


