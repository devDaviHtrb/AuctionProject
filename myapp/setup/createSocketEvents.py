import pkgutil
from importlib import import_module

def create_SocketEvents() -> None:
    folder = "myapp/sockets"

    #Using pkgutil for read all modules in the folder
    for ignore1, module, ignore2 in pkgutil.iter_modules([folder]):
        #importing the event with import_module
        import_module(f"myapp.sockets.{module}")
        