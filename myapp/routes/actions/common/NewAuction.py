from flask import Blueprint, Response, request, jsonify
from myapp.models.Products import products
from myapp.models.TechnicalFeaturesValues import technical_features_values
from myapp.utils.Validations.GeneralProductValidation import general_validation
from typing import Tuple

newAuction = Blueprint("newAuction", __name__)

@newAuction.route("/newAuction", methods=["POST"])
def NewAuction() -> Tuple[Response, int]:
    data, code = general_validation(request)
    print("foi validado")
    if(code != 200):
        return data, code

    product = products.save_item(data)

    necessary_technical_features = product.get_technical_feature_id()


    for technical_feature in necessary_technical_features:
        feature_id =        technical_feature.technical_feature_id 
        feature_name =      technical_feature.technical_feature_name
        value = request.form.get(feature_name, None)
        technical_features_values.save_item({
            "value":                value, #CONTENT
            "product_id":           product.product_id,
            "category_id":          product.category,
            "technical_feature_id": feature_id
        })
    return jsonify({
        "Type": "created"
    }), 201
