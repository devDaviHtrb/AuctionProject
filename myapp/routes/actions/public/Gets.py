from flask import Blueprint, Response, jsonify
from myapp.utils.LinksUrl import get_search_links
import myapp.repositories.CategoryRepository as category_repository
from typing import Tuple

gets_bp = Blueprint("gets", __name__)

@gets_bp.route("/get/searchs-info")
def serchs_info() -> Tuple[Response, int]:
    return jsonify(get_search_links()), 200

@gets_bp.route("/get/relationship/categories")
def get_relationship_categories() -> Tuple[Response, int]:
    relatioship = category_repository.get_relationship_categories_features()
    #convert
    for key in relatioship:
        for i in range(len(relatioship[key])):
            relatioship[key][i] = relatioship[key][i].technical_feature_name

    return jsonify(relatioship), 200