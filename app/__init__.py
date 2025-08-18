from flask import blueprints, Flask
from flask_socketio import SocketIO
def create_app():

    app = Flask(__name__)
    app.secret_key = 'senha'
    socketIo = SocketIO(app, cors_allowed_origins="*")  
    
    #Listing blueprints
    

    #Returning instance
    return {"app":app, "socket":socketIo}


