import pkgutil
from importlib import import_module
from inspect import getmembers
from flask import Blueprint, Flask
import os



def register_routes(app: Flask, folder:str="myapp/routes", package:str="myapp.routes") -> None:
    folder = os.path.abspath(folder)
    for item in os.listdir(folder):

        if  item!="__pycache__":
            #verifying if is a module
            if item.endswith(".py") == False:
                #opening the folder

                SubDirectory = f"{folder}/{item}"
                SubDirectoryPackage = f"{package}.{item}"

                register_routes(app, SubDirectory, SubDirectoryPackage)
            else:
                module_name = f"{package}.{item[:-3]}" #removing: .py
                module = import_module(module_name)

                for ignore1, obj in getmembers(module):
                    if isinstance(obj, Blueprint):
                        app.register_blueprint(obj)