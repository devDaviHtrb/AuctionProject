from myapp.extensions import *

def init_extensions(app):

    init_image_db()
    
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



    return socketIo