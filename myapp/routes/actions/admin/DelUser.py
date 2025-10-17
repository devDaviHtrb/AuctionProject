from flask import Blueprint, request, Response, jsonify
from myapp.models.Users import users
from typing import Tuple

delete_user = Blueprint("DelUser", __name__)

@delete_user.route("/delete/user/<int:user_id>", methods = ["DELETE"])
def del_user(user_id:int) -> Tuple[Response, int]:
    user = users.query.get(user_id)
    if (not user):
        return jsonify({"Error": "Not Found Id"}), 400
    success, expt = user.delete()
    if(success):
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    return jsonify({"Error": str(expt)}), 500