from importlib import import_module
from inspect import getmembers
from flask import Blueprint, Flask
import os
from myapp.setup.PermissionRequire import commonRoutes, publicRoutes, adminRoutes

permissionLevel_list = {
    "public": publicRoutes,
    "admin": adminRoutes,
    "common": commonRoutes,
}

def get_blueprint_endPoints(obj):
    temp_app = Flask("temp_app")
    temp_app.register_blueprint(obj)
    endpoints = [rule.endpoint for rule in temp_app.url_map.iter_rules()]
    del temp_app
    return endpoints

def register_routes(app: Flask, folder:str="myapp/routes", package:str="myapp.routes") -> None:
    #folder = os.path.abspath(folder)
    
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
        
        module_name = f"{package}.{item[:-3]}" #removing: .py print(  )
        module = import_module(module_name)
        # *****too expansive, fix later*****
        for _, obj in getmembers(module):
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj)
                folder_permission_level = os.path.basename(folder)
                permissionLevel_list[folder_permission_level].extend(get_blueprint_endPoints(obj))

        print(f"Admin:{adminRoutes} \nPublicas:{publicRoutes}\nComuns:{commonRoutes}")