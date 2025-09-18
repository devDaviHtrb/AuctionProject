from flask import *
from myapp.setup.InitSocket import init_socket
from myapp.setup.InitiLoginManager import init_loginManager
from config import Config
from myapp.setup.InitSqlAlchemy import init_db
from myapp.setup.createSocketEvents import create_SocketEvents
from myapp.setup.createTables import create_tables
from myapp.setup.registerRoutes import register_routes