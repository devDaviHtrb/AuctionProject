from flask import Blueprint, jsonify, abort
from myapp.repositories.UserRepository import force_logout_all as force_all
from myapp.repositories.UserRepository import force_logout_user as force_user
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/forceLogoutUser/<username>", methods=["POST", "GET"])
def force_logout_user(username):
   
    if not username:
        abort(400, description="Write the username (username).")

    force_user(username)

    return jsonify({"message": f"User '{username}' was forced to logout if who isn't an administrator."}), 200


@admin_bp.route("/forceLogoutAll", methods=["POST", "GET"])
def force_logout_all():
    
    force_all()

    return jsonify({"message": "All the not administrator users was forced to logout."}), 200
