import pkgutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

def write_file(src:str, content:str) -> None:
    with open(src, 'a') as file:
        file.write(content)

def create_tables(app:Flask, db:SQLAlchemy) -> None:
    FOLDER = "myapp/models"
    DATABASE_SRC = "database.sql"

    #Using pkgutil for read all modules in the FOLDER
    for ignore1, model, ignore2 in pkgutil.iter_modules([FOLDER]):
        #importing the model with import_module
        import_module(f"myapp.models.{model}")
    
    #using the db in app
    with open(DATABASE_SRC, 'w') as file:
        file.write('')

    with app.app_context():
        db.create_all()
        dialect = postgresql.dialect()
        write_file(DATABASE_SRC,"\n-- === SQL CREATE TABLES ===\n")
        for table in db.metadata.sorted_tables:
            if dialect:
                sql = str(CreateTable(table).compile(dialect=dialect))
            else:
                sql = str(CreateTable(table))
            sql += '\n'
            write_file(DATABASE_SRC, sql)