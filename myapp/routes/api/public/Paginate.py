from flask import Blueprint, abort, jsonify, session
from flask import Response
from myapp.models.Categories import categories
from myapp.models.Products import products
from myapp.models.Users import users
from myapp.models.Images import images
from typing import Tuple

paginate_bp = Blueprint("paginate", __name__)

@paginate_bp.route("/paginate/<type>/<int:page>", methods=["GET"])
@paginate_bp.route("/paginate/<type>/<int:page>/<filter_select>", methods=["GET"])
def paginate(type:str, page:int, filter_select:str=None) -> Tuple[Response, int]:
    current_page = page
    auctions_per_page = 10 #this value needs to be defined
    if type == "auctions":
        products_list = products.query.order_by(products.product_id).paginate(
            page =      current_page,
            per_page =  auctions_per_page
        )
    elif type=="myItens":
        user = users.query.filter_by(
            user_id = session.get("user_id", None)
        ).first() 
        if user:
            products_list = products.query.filter_by(user_id=user.user_id).paginate(
                page =      current_page,
                per_page =  auctions_per_page
            )
        else:
            abort(401)
            return jsonify({
                "Error": "No access"
            }) , 401
    else:
        return jsonify({
            "Error": "Query error, this route not exists"
        }), 400
    categories_list = {
        current_category.category_id: current_category.category_name for current_category in categories.query.order_by(categories.category_id).all()
    }

    if filter_select and type=="auctions":
        print(filter_select)
        category = categories.query.filter_by(category_name = filter_select).first()
        if category:
            products_list = products.query.filter_by(category_id=category.category_id).paginate(page=current_page, per_page=auctions_per_page)
        else:
            return jsonify({
                "Error": "query error, this category not exists"
            }), 400
    
    products_response = [
        {
            "product_name":     product.product_name,
            "description":      product.description,
            "min_bid":          str(product.min_bid) if product.min_bid is not None else None,
            "start_datetime":   product.start_datetime.isoformat() if product.start_datetime else None,
            "category":         categories_list.get(product.category_id),
            "room":             product.product_room,
            "photo":            images.query.filter_by(product_id = product.product_id).first()
        } for product in products_list.items
    ]
                
    response = {
        "products":     products_response,
        "current_page": products_list.page,
        "total_pages":  products_list.pages,
        "has_next":     products_list.has_next,
        "has_prev":     products_list.has_prev
    }

    return jsonify(response), 200