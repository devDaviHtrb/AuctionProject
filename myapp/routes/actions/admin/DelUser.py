from flask import Blueprint, request

delete_user = Blueprint("DelUser", __name__)

@delete_user.route("/delete_user", methods = ["POST"])
def del_user():
    pass