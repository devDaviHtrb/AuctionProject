
from .extensions import *
from flask import Flask
from flask_socketio import SocketIO
from typing import Tuple

def create_app() -> Tuple[Flask, SocketIO]:

    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    #Listing blueprints
    register_routes(app)
    register_handlers(app)
    #Socket initialization
    socketIo = init_socket(app) 
    create_SocketEvents()
    
    #Db initialization
    db = init_db(app)
    create_tables(app, db)

    init_loginManager(app)

    init_authDecorator(app)
    

    #Returning instance
    return app, socketIo


