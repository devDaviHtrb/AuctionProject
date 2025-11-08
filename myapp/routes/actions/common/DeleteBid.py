from flask import Blueprint, Response, session, jsonify
from myapp.setup.InitSocket import socket_io
from myapp.models.Bids import bids
from myapp.models.Products import products
from myapp.setup.InitSqlAlchemy import db
from typing import Tuple
from sqlalchemy import delete, select

del_auction_bp = Blueprint("delAuction", __name__)

@del_auction_bp.route("/del/bid/<int:product_id>", methods = ["DELETE"])
def del_auction(product_id:int) -> Tuple[Response, int]:
    user_id = session["user_id"]
    print(user_id)
    room_id = db.session.execute(
        select(products.product_room).where(
            products.product_id == product_id
        )
    ).scalar()

    stmt = delete(bids).where(
        bids.product_id == product_id,
        bids.user_id == user_id
    )
    db.session.execute(stmt)
    db.session.commit()
    response = {
        "type": "delete",
    }

    socket_io.emit("server_content", {"response": response}, to = room_id)
    return jsonify({"status": "ok"}), 200