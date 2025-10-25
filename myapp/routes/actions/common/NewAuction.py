from flask import Blueprint, Response, request, jsonify
from myapp.utils.Validations.GeneralProductValidation import general_validation
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.TechnicalFeatureValueRepository as tch_feat_val_repository
from typing import Tuple

newAuction_bp = Blueprint("newAuction", __name__)

@newAuction_bp.route("/new/Auction", methods=["POST"])
def new_auction() -> Tuple[Response, int]:
    data, code = general_validation(request)
    print("foi validado")
    if(code != 200):
        return data, code

    product = product_repository.save_item(data)

    necessary_technical_features = product_repository.get_technical_feature_id(product)


    for technical_feature in necessary_technical_features:
        feature_id =        technical_feature.technical_feature_id 
        feature_name =      technical_feature.technical_feature_name
        value =             request.form.get(feature_name, None)
        tch_feat_val_repository.save_item({
            "value":                value, #CONTENT
            "product_id":           product.product_id,
            "category_id":          product.category,
            "technical_feature_id": feature_id
        })
    return jsonify({
        "Type": "created"
    }), 201
