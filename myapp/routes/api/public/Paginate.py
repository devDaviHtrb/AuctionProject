from flask import Blueprint, jsonify, session
from flask import Response, request
from myapp.models.Categories import categories
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
from myapp.models.Images import images
from typing import Tuple
from sqlalchemy import asc, desc, case

OCCURRING = "Ativo"

paginate_bp = Blueprint("paginate", __name__)

@paginate_bp.route("/paginate/<type>/<int:page>", methods=["GET"])
def paginate(type: str, page: int) -> Tuple[Response, int]:
    current_page = page
    items_per_page = 9

    category_name = request.args.get("category")
    status_filter = request.args.get("status")
    name_filter = request.args.get("name")
    price_range = request.args.get("price_range")
    sort_type = request.args.get("sort")

    query = products.query

    if type == "myItems":
        user_id = session.get("user_id", None)
        if not user_id:
            return jsonify({"Error": "No access"}), 401
        query = query.filter_by(user_id=user_id)

    if name_filter:
        query = query.filter(products.product_name.ilike(f"%{name_filter}%"))

    if category_name:
        category = categories.query.filter_by(category_name=category_name).first()
        if not category:
            return jsonify({"Error": "Category not found"}), 400
        query = query.filter_by(category=category.category_id)

    if status_filter:
        status = product_statuses.query.filter(
            product_statuses.product_status == status_filter
        ).first()
        if not status:
            return jsonify({"Error": f"Status '{status_filter}' not found"}), 400
        query = query.filter(products.product_status == status.product_status_id)

    if price_range:
        try:
            min_price, max_price = map(float, price_range.split("-"))
            query = query.filter(products.min_bid >= min_price, products.min_bid <= max_price)
        except ValueError:
            return jsonify({"Error": "Invalid price range format. Use min-max"}), 400

    stat = product_statuses.query.filter_by(product_status=OCCURRING).first()
    active_status_id = stat.product_status_id if stat else None

    if sort_type == "recent_asc":
        query = query.order_by(
            case((products.product_status == active_status_id, 0), else_=1),
            asc(products.start_datetime)
        )
    elif sort_type == "recent_desc":
        query = query.order_by(
            case((products.product_status == active_status_id, 0), else_=1),
            desc(products.start_datetime)
        )
    elif sort_type == "price_asc":
        query = query.order_by(
            case((products.product_status == active_status_id, 0), else_=1),
            asc(products.min_bid)
        )
    elif sort_type == "price_desc":
        query = query.order_by(
            case((products.product_status == active_status_id, 0), else_=1),
            desc(products.min_bid)
        )
    else:
        query = query.order_by(
            case((products.product_status == active_status_id, 0), else_=1),
            products.product_id
        )

    paginated_products = query.paginate(
        page=current_page,
        per_page=items_per_page
    )

    categories_dict = {
        cat.category_id: cat.category_name for cat in categories.query.order_by(categories.category_id).all()
    }

    products_response = []
    for product in paginated_products.items:
        image_obj = images.query.filter_by(product_id=product.product_id).first()
        photo_url = {"photo_url": image_obj.image} if image_obj else None

        products_response.append({
            "product_name": product.product_name,
            "description": product.description,
            "min_bid": str(product.min_bid) if product.min_bid else None,
            "start_datetime": product.start_datetime.isoformat() if product.start_datetime else None,
            "duration": product.duration,
            "category": categories_dict.get(product.category),
            "room": product.product_room,
            "photo_url": photo_url
        })

    response = {
        "products": products_response,
        "current_page": paginated_products.page,
        "total_pages": paginated_products.pages,
        "has_next": paginated_products.has_next,
        "has_prev": paginated_products.has_prev
    }

    return jsonify(response), 200
