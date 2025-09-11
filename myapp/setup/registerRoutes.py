import pkgutil
from importlib import import_module
from inspect import getmembers
from flask import Blueprint
import os



def register_routes(app, folder="myapp/routes", package="myapp.routes"):
    folder = os.path.abspath(folder)
    for item in os.listdir(folder):

        if  item!="__pycache__":
            #verifying if is a module
            if item.endswith(".py") == False:
                #opening the folder
                register_routes(app, f"{folder}/{item}", f"{package}.{item}")
            else:

                module = import_module(f"{package}.{item[:-3]}")

                for ignore1, obj in getmembers(module):
                    if isinstance(obj, Blueprint):
                        app.register_blueprint(obj)