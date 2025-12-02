from flask import Flask
from flask_socketio import SocketIO
from typing import Tuple
from myapp.config import Config
from myapp.context import init_context
from myapp.setup.MakeInsert import all_inserts
from myapp.initExtensions import init_extensions

def create_app() -> Tuple[Flask, SocketIO]:

    app = Flask(__name__)
    app.config.from_object(Config)
    
    socketIo = init_extensions(app) #return socket object
    with app.app_context():
        all_inserts()
    init_context(app)

    #Returning instance
    return app, socketIo


