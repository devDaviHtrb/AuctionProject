from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app:Flask) -> SQLAlchemy:
    db.init_app(app)
    return db