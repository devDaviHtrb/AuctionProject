from flask import Blueprint, Response, session, jsonify
from myapp.setup.InitSocket import socket_io
from typing import Tuple
import myapp.repositories.ProductRepository as product_repository

del_auction_bp = Blueprint("delAuction", __name__)

@del_auction_bp.route("/del/bid/<int:product_id>", methods = ["DELETE"])
def del_auction(product_id:int) -> Tuple[Response, int]:
    user_id = session["user_id"]
    print(user_id)
    room_id = product_repository.get_room_id_by_id(product_id)
    
    response = {
        "type": "delete",
    }

    socket_io.emit("server_content", {"response": response}, to = room_id)
    return jsonify({"status": "ok"}), 200