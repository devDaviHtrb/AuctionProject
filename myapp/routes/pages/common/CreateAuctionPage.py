from flask import Blueprint, render_template
import myapp.repositories.CategoryRepository as category_repository

create_auction_page_bp = Blueprint("createAuctionPage", __name__)
@create_auction_page_bp.route("/form/auction")
def CreateAuctionPage():
    return render_template(
        "CreateAuctionPage.html",
    )