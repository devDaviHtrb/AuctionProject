from flask import Blueprint, render_template, request, session
from myapp.repositories.GetBids import get_interesting_user_bids
user_bids_bp = Blueprint("userBids", __name__)

@user_bids_bp.route("/userBidsPage")
def user_bids_page():
    user_id = session.get("user_id")
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status", "active")
    sort = request.args.get("sort", "time")

    bids_dict = get_interesting_user_bids(
        user_id=user_id,
        page=page,
        status=status,
        sort=sort
    )

    return render_template(
        "UserBidsPage.html",
        bids=bids_dict["bids"],
        active_number=bids_dict["active_bids_number"],
        winner_number=bids_dict["winner_bids_number"],
        pagination=bids_dict["pagination"],
        current_status=status,
        current_sort=sort
    )