from flask import Blueprint, render_template, session
from myapp.repositories.GetBids import get_interesting_user_bids
user_bids_bp = Blueprint("userBids", __name__)

@user_bids_bp.route("/userBidsPage")
def user_bids_page():
        bids_dict = get_interesting_user_bids(session.get("user_id", None))
        return render_template("UserBidsPage.html", bids = bids_dict["bids"], active_number= bids_dict["active_bids_number"], winner_number=bids_dict["winner_bids_number"])