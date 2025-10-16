# setup/register_handlers.py
import pkgutil
from flask import Flask, render_template
from typing import Tuple

def register_handlers(app: Flask) -> None:
    error_codes = [403, 404, 401]
    error_pages = {}
    
    for code in error_codes:
        error_pages[code] = f"{code}.html"

    def handle_error(err: object) -> Tuple[str, int]:
        code = getattr(err, "code")
        # Closure: this function is called when an error is aborted, so it can remember and access the error_pages dictionary because it is in the scope of the register_handlers function.
        template = error_pages.get(code) 
        return render_template(template), code

    for code in error_pages:
        app.register_error_handler(code, handle_error)