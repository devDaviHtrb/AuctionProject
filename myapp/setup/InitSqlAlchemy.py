from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
<<<<<<< HEAD
def init_db(app):
=======

def init_db(app:Flask) -> SQLAlchemy:
>>>>>>> WebSocketIO
    db.init_app(app)
    return db