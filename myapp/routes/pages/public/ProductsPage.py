from flask import render_template, Blueprint, Response, request
from urllib.parse import urlencode
import myapp.repositories.CategoryRepository as category_repository
import myapp.repositories.ProductStatusRepository as product_status_repository
from myapp.utils.Async import run_async_functions

products_page_bp = Blueprint("productsPage", __name__)

@products_page_bp.route("/products")
@products_page_bp.route("/products/<int:page>")
def ProductsPage(page: int = 1) -> Response:

    results = run_async_functions([
        (category_repository.get_categories_frequency,(),{},)
        (product_status_repository.get_status_frequencies, (), {})
    ])

    categories_amt =    results[0]
    status_amt =        results[1]

    query_params = {key: request.args[key] for key in request.args}
    paginate_args = f"/paginate/auctions/{page}?{urlencode(query_params)}"

    return render_template(
        "Products.html",
        paginate_args=paginate_args,
        categories_amt=categories_amt,
        status_amt=status_amt
    )
