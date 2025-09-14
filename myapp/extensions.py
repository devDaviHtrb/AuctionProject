from flask import *
from myapp.setup.InitSocket import init_socket
from config import Config
from myapp.setup.InitSqlAlchemy import init_db
from myapp.setup.CreateSocketEvents import create_SocketEvents
from myapp.setup.CreateTables import create_tables
from myapp.setup.RegisterRoutes import register_routes