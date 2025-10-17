from flask import *
from flask_socketio import SocketIO
from myapp.setup.InitSocket import init_socket

from myapp.setup.InitSqlAlchemy import init_db
from myapp.setup.createSocketEvents import create_SocketEvents
from myapp.setup.createTables import create_tables
from myapp.setup.registerRoutes import register_routes

from myapp.setup.PermissionRequire import init_authDecorator
from myapp.setup.registerHandlers import register_handlers
from myapp.setup.InitSqlAlchemy import db
from myapp.setup.InitImageDb import init_image_db