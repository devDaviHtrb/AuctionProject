
from .extensions import *

def create_app():

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


