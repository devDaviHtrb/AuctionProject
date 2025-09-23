from importlib import import_module
from inspect import getmembers
from flask import Blueprint, Flask
import os
from myapp.setup.PermissionRequire import commonRoutes, publicRoutes, adminRoutes

def register_routes(app: Flask, folder:str="myapp/routes", package:str="myapp.routes") -> None:
    folder = os.path.abspath(folder)
    for item in os.listdir(folder):
        if  item =="__pycache__":
            continue
            #verifying if is a module

        pathRoute = os.path.join(folder, item) 

        #opening the folder
        if os.path.isdir(pathRoute): 
            register_routes(app, pathRoute, f"{package}.{item}")
            continue

        # "{blueprint name}.{blueprint arquive name}"
        module_name = f"{package}.{item[:-3]}" #removing: .py
        module = import_module(module_name)
            
        for ignore1, obj in getmembers(module):
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj)
                route_name = f"{obj.name}.{obj.name.capitalize()}"
                match os.path.basename(folder):
                    case "public":
                        publicRoutes.append(route_name)
                    case "admin":
                        adminRoutes.append(route_name)
                    case "common":
                        commonRoutes.append(route_name)