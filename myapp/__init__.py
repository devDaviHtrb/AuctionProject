from config import Config
from flask import Flask
from flask_socketio import SocketIO
from typing import Tuple

from myapp.initExtensions import init_extensions

def create_app() -> Tuple[Flask, SocketIO]:

    app = Flask(__name__)
    app.config.from_object(Config)
    
    socketIo = init_extensions(app) #return socket object

    #Returning instance
    return app, socketIo


