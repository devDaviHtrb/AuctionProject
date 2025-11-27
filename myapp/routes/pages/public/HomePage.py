from flask import render_template, Blueprint, Response

from myapp.repositories.ProductRepository import get_and_images_and_status_diffents_valids_randomly

home = Blueprint("homePage", __name__)

@home.route("/")
def HomePage() -> Response:
    return render_template(
       
        "Index.html",
        # fix it
        top_products = [
            {
                "photo": "#",
                "name":  "A",
                "price": 3.2,
                "time": 3000
            },
            {
                "photo": "#",
                "name":  "A",
                "price": 3.2,
                "time": 3000
            },
            {
                "photo": "#",
                "name":  "A",
                "price": 3.2,
                "time": 3000
            },
            {
                "photo": "#",
                "name":  "A",
                "price": 3.2,
                "time": 3000
            }
         ]
    )
