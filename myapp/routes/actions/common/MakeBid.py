from flask import Blueprint, request, redirect, url_for, flash, session
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Products import products
from myapp.services.BidService import make_bid 

bid_routes = Blueprint("bid_routes", __name__)

@bid_routes.route("/make_bid", methods=["POST"])
def make_bid_route():
    try:
        user_id = session.get("user_id")

        product_id = request.form.get("product_id", type=int)
        bid_value = request.form.get("bid_value", type=float)

        if not product_id or not bid_value:
            flash("Dados inválidos.", "error")
            return redirect(url_for("userBids.user_bids_page")) #the flash messages are in portuguese because in order to use the same language of the front end

        product = products.query.get(product_id)

        if not product:
            flash("Produto não encontrado.", "error")
            return redirect(url_for("userBids.user_bids_page"))

        success, response = make_bid(user_id, product, bid_value)

        if success:
            flash("Lance realizado com sucesso!", "success")
            return redirect(request.referrer)

        
        flash(response["msg"], "error")
        redirect(url_for("userBids.user_bids_page"))

    except Exception as e:
        print("Error:", e)
        flash("Erro inesperado ao fazer lance.", "error")
        return redirect(request.referrer)
