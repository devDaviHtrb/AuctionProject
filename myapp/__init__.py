from config import Config
from flask import Flask
from flask_socketio import SocketIO
from typing import Tuple
from myapp.context import init_context
from myapp.initExtensions import init_extensions

def create_app() -> Tuple[Flask, SocketIO]:

    app = Flask(__name__)
    app.config.from_object(Config)
    
    socketIo = init_extensions(app) #return socket object
    init_context(app)

    #Returning instance
    return app, socketIo


