from myapp.extensions import *
from myapp.services.ProductService import restart_closes, restart_open

def init_extensions(app: Flask) -> SocketIO:
    
    #Socket initialization
    socket_io = init_socket(app) 
    create_SocketEvents()

    #Flask Cache
    init_cache(app)
    
    #Db initialization
    db = init_db(app)

    create_tables(app, db)

    init_authDecorator(app)

    #Listing blueprints
    register_routes(app)
    register_handlers(app)

    with app.app_context():
        restart_open()
        restart_closes()

    return socket_io