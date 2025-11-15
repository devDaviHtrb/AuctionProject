from flask import Blueprint, abort, jsonify, session
from flask import Response, request
from myapp.models.Categories import categories
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
from myapp.models.Users import users
from myapp.models.Images import images
from typing import Tuple

paginate_bp = Blueprint("paginate", __name__)

@paginate_bp.route("/paginate/<type>/<int:page>", methods=["GET"])
def paginate(type: str, page: int) -> Tuple[Response, int]:
    current_page = page
    items_per_page = 9  # number of products per page

    # Get optional filters from query parameters
    category_name = request.args.get("category")

    status_filter = request.args.get("status")
    name_filter = request.args.get("name")
    price_range = request.args.get("price_range")  # e.g., "100-500"

    query = products.query

    # Filter by type of page
    if type == "auctions":
        pass  # all products by default, filters applied below
    elif type == "myItems":
        user_id=session.get("user_id", None)
        if not user_id:
            return jsonify({"Error": "No access"}), 401
        query = query.filter_by(user_id=user_id)


    if name_filter:
        query = query.filter(products.product_name.ilike(f"%{name_filter}%"))

    # Filter by category
    if category_name:
        category = categories.query.filter_by(category_name=category_name).first()
        if not category:
            return jsonify({"Error": "Category not found"}), 400
        query = query.filter_by(category=category.category_id)

    # Filter by status (e.g., 'active', 'sold')
    if status_filter:
        # busca case-insensitive pelo nome do status
        status = product_statuses.query.filter(
            product_statuses.product_status == status_filter.lower()
        ).first()

        if not status:
            return jsonify({"Error": f"Status '{status_filter}' not found"}), 400

        # filtra produtos que têm esse status
        query = query.filter(products.product_status == status.product_status_id)

    # Filter by price range
    if price_range:
        try:
            min_price, max_price = map(float, price_range.split("-"))
            query = query.filter(products.min_bid >= min_price, products.min_bid <= max_price)
        except ValueError:
            return jsonify({"Error": "Invalid price range format. Use min-max"}), 400

    # Apply pagination
    paginated_products = query.order_by(products.product_id).paginate(
        page=current_page,
        per_page=items_per_page
    )

    # Build categories dictionary
    categories_dict = {
        cat.category_id: cat.category_name for cat in categories.query.order_by(categories.category_id).all()
    }

    # Build response
    products_response = [
        {
            "product_name": product.product_name,
            "description": product.description,
            "min_bid": str(product.min_bid) if product.min_bid else None,
            "start_datetime": product.start_datetime.isoformat() if product.start_datetime else None,
            "category": categories_dict.get(product.category),
            "room": product.product_room,
            #fix it
            "photo_url": images.query.filter_by(product_id=product.product_id).first().image if images.query.filter_by(product_id=product.product_id).first() else "#"
        }
        for product in paginated_products.items
    ]

    response = {
        "products": products_response,
        "current_page": paginated_products.page,
        "total_pages": paginated_products.pages,
        "has_next": paginated_products.has_next,
        "has_prev": paginated_products.has_prev
    }


    return jsonify(response), 200
