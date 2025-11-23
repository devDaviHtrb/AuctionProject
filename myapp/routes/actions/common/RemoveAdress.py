from flask import Blueprint, request, redirect, session, url_for
from myapp.models.Addresses import addresses
from myapp.models.Users import users
from myapp.setup.InitSqlAlchemy import db
from myapp.utils.LinksUrl import CONFIG_PAGE

removeAddress = Blueprint("removeAdress", __name__)


@removeAddress.route("/removeAddress/<int:address_id>", methods=["POST"])
def remove_address(address_id):
    addr = addresses.query.get(address_id)
    if not addr or addr.user_id != session.get("user_id"):
        return redirect(url_for(CONFIG_PAGE, msg="Invalid address"))
    
    db.session.delete(addr)
    db.session.commit()
    return redirect(url_for(CONFIG_PAGE, msg="Address removed"))