from flask import render_template, Blueprint, Response, session

from myapp.repositories.GetBids import get_interesting_user_bids


profile = Blueprint("profile", __name__)


@profile.route("/profile")

def Profile() -> Response:
    user_bids = get_interesting_user_bids(user_id=session.get("user_id"))
    return render_template("Profile.html", bids = [bid for bid in user_bids if user_bids.index(bid)<=2])