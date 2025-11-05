from flask import render_template, Blueprint, Response, request
from urllib.parse import urlencode
import myapp.repositories.CategoryRepository as category_repository
import myapp.repositories.ProductStatusRepository as product_status_repository

products_page_bp = Blueprint("productsPage", __name__)

@products_page_bp.route("/products")
@products_page_bp.route("/products/<int:page>")
def ProductsPage(page: int = 1) -> Response:
    CATEGORIES_AMT = category_repository.get_categories_frequency()
    STATUS_AMT = product_status_repository.get_status_frequencies()

    query_params = {key: request.args[key] for key in request.args}
    paginate_args = f"/paginate/auctions/{page}?{urlencode(query_params)}"

    return render_template(
        "Auctions.html",
        paginate_args=paginate_args,
        categories_amt=CATEGORIES_AMT,
        status_amt=STATUS_AMT
    )
