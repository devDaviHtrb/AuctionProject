from flask import blueprints, Flask
from flask_socketio import SocketIO
from config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    socketIo = SocketIO(app)  
    
    #Listing blueprints
    #Importing sockets events
    from app import sockets

    #Returning instance
    return {"app":app, "socket":socketIo}


