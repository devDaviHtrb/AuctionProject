from flask import Blueprint, Response, session, jsonify
from myapp.setup.InitSocket import socket_io
from typing import Tuple
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.UserRepository as user_repository

del_auction_bp = Blueprint("delAuction", __name__)

OCCURRING = "Ativo"

@del_auction_bp.route("/del/bid/<int:product_id>", methods = ["DELETE"])
def del_auction(product_id:int) -> Tuple[Response, int]:
    user_id = session["user_id"]
    print(user_id)
    product = product_repository.get_by_id(product_id)
    status = product_repository.get_status(product)
    room_id = product.product_room
    if(status.lower() != OCCURRING):
        return jsonify({"status": "error"}), 400
    user_repository.delete_bids_by_product_id_user_id(user_id, product_id)
    
    response = {
        "type": "delete",
    }

    socket_io.emit("server_content", {"response": response}, to = room_id)
    return jsonify({"status": "ok"}), 200