from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask

db = SQLAlchemy()
SessionLocal = None

def init_db(app: Flask):
    global SessionLocal
    
    db.init_app(app)

    with app.app_context():
        engine = db.engine
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    return db

def get_session():
    global SessionLocal
    if SessionLocal is None:
        raise RuntimeError("SessionLocal accessed before initialization")
    return SessionLocal()
