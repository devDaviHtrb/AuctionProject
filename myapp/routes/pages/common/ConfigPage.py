from flask import render_template, Blueprint, request, session
from myapp.models.Addresses import addresses
from myapp.repositories.GetBids import get_interesting_user_bids 

configPage = Blueprint("configPage", __name__)

@configPage.route("/configPage")
@configPage.route("/configPage/<msg>")
def ConfigPage(msg=None):
    uid = session["user_id"]


  
    page = int(request.args.get("page", 1))
    per_page = 3


    user_addresses = addresses.query.filter_by(user_id=uid).all()



    return render_template(
    "Config.html",
    email=session.get("email"),
    username=session.get("username"),
    name=session.get("name"),
    msg=msg,
    photo=session.get("user_photo"),
    user_type=session.get("user_type"),
    gender=session.get("gender"),
    cellphone1=session.get("cellphone1", ""),
    cellphone2=session.get("cellphone2", ""),
    landline=session.get("landline", ""),
    cpf=session.get("cpf", None),
    rg=session.get("rg", None),
    trade_name=session.get("trade_name", None),
    state_tax_registration=session.get("state_tax_registration", None),
    legal_business_name=session.get("legal_business_name", None),
    addresses=user_addresses,

)


@configPage.route("/api/bids")
def api_bids():
    uid = session["user_id"]

    page = int(request.args.get("page", 1))
    per_page = 3

    user_bids = get_interesting_user_bids(uid)

    total_bids = len(user_bids)
    total_pages = (total_bids + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    paginated = user_bids[start:end]

    return {
        "page": page,
        "total_pages": total_pages,
        "bids": [
            {
                "product_name": b["product"].product_name,
                "amount": float(b["bid"].bid_value),
                "room": b["product"].product_room,
                "status": b["status"]
            }
            for b in paginated
        ]
    }

