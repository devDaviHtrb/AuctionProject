from myapp.utils.File import erase_file, write_file 
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from flask import Flask
import pkgutil

def drop_all_tables(db: SQLAlchemy) -> None:
    try:
        db.drop_all()  
        db.session.commit()
        print("reset Tables")
    except Exception as e:
        db.session.rollback()
        print(f"error {e}")


def create_tables(app:Flask, db:SQLAlchemy) -> None:
    FOLDER = "myapp/models"
    DATABASE_SRC = "database.sql"

    #Using pkgutil for read all modules in the FOLDER
    for ignore1, model, ignore2 in pkgutil.iter_modules([FOLDER]):
        #importing the model with import_module
        import_module(f"myapp.models.{model}")
    
    #using the db in app
    #erase_file(DATABASE_SRC)

    with app.app_context():
        #drop_all_tables(db) #:O
        db.create_all()
        dialect = postgresql.dialect()
        #write_file(DATABASE_SRC, HEADER)
        for table in db.metadata.sorted_tables:
            if dialect:
                sql = str(CreateTable(table).compile(dialect=dialect))
            else:
                sql = str(CreateTable(table))
            sql += '\n'
            #write_file(DATABASE_SRC, sql)