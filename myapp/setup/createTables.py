import pkgutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

def create_tables(app:Flask, db:SQLAlchemy) -> None:
    folder = "myapp/models"

    #Using pkgutil for read all modules in the folder
    for ignore1, model, ignore2 in pkgutil.iter_modules([folder]):
        #importing the model with import_module
        import_module(f"myapp.models.{model}")
    
    #using the db in app
    with app.app_context():
        db.create_all()