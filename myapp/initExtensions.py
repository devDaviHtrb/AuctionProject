from myapp.extensions import *

def init_extensions(app: Flask) -> SocketIO:
  
    
    #Listing blueprints

    #Socket initialization
    socket_io = init_socket(app) 
    create_SocketEvents()

    #Flask Cache
    init_cache(app)
    
    #Db initialization
    db = init_db(app)

    create_tables(app, db)

    init_authDecorator(app)

    register_routes(app)
    register_handlers(app)

    return socket_io