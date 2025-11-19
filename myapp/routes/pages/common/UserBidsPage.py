from flask import Blueprint, render_template

user_bids_bp = Blueprint("userBids", __name__)

@user_bids_bp.route("/userBidsPage")
def user_bids_page():
        return render_template("UserBidsPage.html")