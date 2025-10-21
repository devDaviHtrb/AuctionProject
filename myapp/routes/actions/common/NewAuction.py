from flask import Blueprint, Response, request
from myapp.models.Products import products
from myapp.models.CategoryTechnicalFeatures import category_technical_features
from myapp.utils.Validations.GeneralProductValidation import general_validation
from typing import Tuple, Dict, Any

auction_bp = Blueprint("newAuction", __name__)

@auction_bp.route("/auction/new", methods=["POST"])
def new_auction() -> Tuple[Response, int]:
    data, code = general_validation(request)
    if(code != 200):
        return data, code

    products.save_item(data)