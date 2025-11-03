from flask import Blueprint, Response, jsonify
from myapp.utils.LinksUrl import get_search_links
import myapp.repositories.CategoryRepository as category_repository
from typing import Tuple

SEARCHS_INFO = None

gets_bp = Blueprint("gets", __name__)

@gets_bp.route("/get/searchs-info")
def serchs_info() -> Tuple[Response, int]:
    global SEARCHS_INFO
    if SEARCHS_INFO is None:
        SEARCHS_INFO = get_search_links()
    return jsonify(SEARCHS_INFO), 200

@gets_bp.route("/get/relationship/categories")
def get_relationship_categories():
    relatioship = category_repository.get_relationship_categories_features()
    #convert
    for key in relatioship:
        for i in range(len(relatioship[key])):
            relatioship[key][i] = relatioship[key][i].technical_feature_name

    return jsonify(relatioship), 200