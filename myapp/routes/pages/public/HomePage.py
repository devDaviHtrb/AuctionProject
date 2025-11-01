from flask import render_template, Blueprint,redirect, session, url_for

home = Blueprint("homePage", __name__)

@home.route("/")
def HomePage():
    return render_template(
        "Index.html",
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


