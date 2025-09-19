# setup/register_handlers.py
import pkgutil
from flask import render_template

def register_handlers(app):
    folder = "myapp/handlers"
    error_pages = {}
    
    for _, module_name, _ in pkgutil.iter_modules([folder]):
        if module_name[:3].isdigit():
            code = int(module_name[:3])
            error_pages[code] = f"{code}.html"

   
    def handle_error(err):
        code = getattr(err, "code", 500)  
        template = error_pages.get(code, "500.html")
        return render_template(template), code


    for code in error_pages:
        app.register_error_handler(code, handle_error)