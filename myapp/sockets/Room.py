from flask_socketio import emit, join_room, rooms
from typing import Dict, Any, List, Optional
from myapp.setup.InitSocket import socket_io
from myapp.models.Products import products
from myapp.models.Bids import bids
import myapp.repositories.ProductRepository as product_repository
from myapp.services.BidService import make_bid
from flask import request, session
from flask_login import current_user

anonymous_users_number = 0

@socket_io.on("join_room")
def handle_join(data: Dict[str, Any]) -> None:
    print(data)
    room_id =   data.get("room_id", None)
    user_id =   session.get("user_id", None)
    username =  session.get("username", None)
    if (None in [room_id, user_id]):
        return
    product = products.query.filter_by(product_room = room_id).first()
    if(not product):
        return
    if(product_repository.get_status(product) != 'occurring'):
        return
    
    join_room(room_id)
    response = {
        "type":     "entry",
        "room_id":  room_id,
        "username": username if not request.cookies.get("anonymous", None) else f"AnonymousUser",
    }

    emit("server_content", {"response": response}, to = room_id)

def get_room_id(auction_rooms: List[str], sid:str) -> Optional[str]:
    if not auction_rooms: 
        return
    if auction_rooms[0] == sid:
        return auction_rooms[1] if len(auction_rooms) > 1 else None
    else:
        return auction_rooms[0]

@socket_io.on("emit_bid")
def handle_emit(data: Dict[str, Any]) -> None:
    room_id = get_room_id(rooms(), request.sid)
    print(">>>", room_id)
 
    user_id =   session.get("user_id", None)
    username =  session.get("username", None)

    value = max(float(data.get("value", 0)), 0)
    product = products.query.filter_by(product_room = room_id).first()
    print(data)

    missingInfo = [i for i in [room_id, value, product] if i is None]

    if missingInfo:
        response = {
            "type": "error",
            "error": "Missing Information",
            "MissingInformation": missingInfo  
        }
        return emit("server_content", {"response":response}, to=request.sid)

    data = {
        "type": "bid",
        "room_id": room_id,
        "username": username if not request.cookies.get("anonymous", None) else f"AnonymousUser",
        "value": value
    }

    flag, out = make_bid(
        user_id =       user_id,
        product =       product,
        value =         value,
    )

    response = data
    if (not flag):
        return emit("server_content", {"response": {"type": "error", "error":out}}, to=request.sid)
    response["datetime"] = out.bid_datetime.isoformat()
    return emit("server_content", {"response": response}, to=room_id)