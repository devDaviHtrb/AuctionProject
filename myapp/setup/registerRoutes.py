import pkgutil
from importlib import import_module
from inspect import getmembers
from flask import Blueprint

def register_routes(app):
    folder = "myapp/routes"

    #Using pkgutil for read all modules in the folder
    for ignore1, route, ignore2 in pkgutil.iter_modules([folder]):
        #importing the module with import_module
        module = import_module(f"myapp.routes.{route}")

        #Returning members(variables, objects, functions and etc)
        instance = getmembers(module)

        for ignore, obj in instance:
            #verifying the type of members
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj)