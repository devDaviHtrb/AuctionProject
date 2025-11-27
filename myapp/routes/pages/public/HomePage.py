from flask import render_template, Blueprint, Response

from myapp.repositories.ProductRepository import get_and_images_and_status_diffents_valids_randomly, get_any

home = Blueprint("homePage", __name__)

@home.route("/")
def HomePage() -> Response:
    return render_template(  
        "Index.html",
        # fix it
        top_products = get_and_images_and_status_diffents_valids_randomly(
            None,
            4
        )
    )
