from flask import Blueprint, jsonify
from myapp.models.Categories import categories
from myapp.models.Products import products

paginate = Blueprint("paginate", __name__)
@paginate.route("/paginate/<int:page>", methods=["GET"])
@paginate.route("/paginate/<int:page>/<filter_select>", methods=["GET"])
def Paginate(page, filter_select=None):
    current_page = page
    auctions_per_page = 10 #this value needs to be defined
    filter_select = filter_select
    products_list = products.query.order_by(products.product_id).paginate(page=current_page, per_page=auctions_per_page)
    categories_list = {current_category.category_id:current_category.category_name for current_category in categories.query.order_by(categories.category_id).all()}

    if filter_select:
        category = categories.query.filter_by(category_name=filter_select).first()
        if category:
            products_list = products.query.filter_by(category_id=category.category_id).paginate(page=current_page, per_page=auctions_per_page)
        else:
            return jsonify("query error")
    
    products_response = [{"product_name": product.product_name,
                 "description":product.description,
                 "min_bid": str(product.min_bid) if product.min_bid is not None else None,
                "start_datetime": product.start_datetime.isoformat() if product.start_datetime else None,
                 "category":  categories_list.get(product.category_id),
                 "room": product.product_room} for product in products_list.items]
                
    response = {
        "products": products_response,
        "current_page": products_list.page,
        "total_pages": products_list.pages,
        "has_next": products_list.has_next,
        "has_prev": products_list.has_prev
    }

    return jsonify(response)