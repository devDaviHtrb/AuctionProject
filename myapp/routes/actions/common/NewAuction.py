from flask import Blueprint, Response, request, jsonify
from myapp.utils.Validations.GeneralProductValidation import general_validation
from myapp.services.ProductService import start_open_timer
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.TechnicalFeatureValueRepository as tch_feat_val_repository
import myapp.repositories.CategoryRepository as category_repository
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Tuple

newAuction_bp = Blueprint("newAuction", __name__)

@newAuction_bp.route("/new/Auction", methods=["POST"])
def new_auction() -> Tuple[Response, int]:
    data, code = general_validation(request)

    if(code != 200):
        return data, code
    
    process_number = request.form.get("process_number",None)
    court = request.form.get("court",None)
    case_type = request.form.get("case_type",None)
    plaintiff = request.form.get("plaintiff",None)
    defendant = request.form.get("defendant",None)
    judge_name = request.form.get("judge_name",None)
    legal_data = {
        "process_number":   process_number,
        "court":            court,
        "case_type":        case_type,
        "plaintiff":        plaintiff,
        "defendant":        defendant,
        "judge_name":       judge_name,
        "extra_notes":      request.form.get("judge_name",None)
    } if(not None in [process_number, court, case_type, plaintiff, defendant, judge_name]) else None
        
    product = product_repository.save_item(data, legal_data)

    necessary_technical_features = category_repository.get_technical_feature_id(product.category)

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

    start_datetime = product.start_datetime
    if(start_datetime):
        start_open_timer(
            product.product_id,
            (start_datetime - datetime.now(ZoneInfo("UTC"))).total_seconds()
        )

    return jsonify({
        "Type": "created"
    }), 201
