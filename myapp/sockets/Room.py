from flask_socketio import emit, join_room, rooms
from typing import Dict, Any, List, Optional
from myapp.setup.InitSocket import socket_io
from myapp.services.MakeBid import make_bid
from flask import request, session


anonymous_users_number = 0

@socket_io.on("join_room")
def handle_join(data: Dict[str, Any]) -> None:
    room_id = data["room_id"]
    if (None in [room_id, session.get("id")]):
        return
    join_room(room_id)
    response = {
        "type": "entry",
        "room_id": room_id,
        "user_id": session.get("id"),
        "username": session.get("username") if not request.cookies.get("anonymous") else f"AnonymousUser{anonymous_users_number}",
    }
    anonymous_users_number+=1
    emit("server_content", {"response": response}, to=room_id)

def get_room_id(auction_rooms: List[str], sid:str) -> Optional[str]:
    if not auction_rooms: 
        return
    if auction_rooms[0] == sid:
        return auction_rooms[1] if len(auction_rooms) > 1 else None
    else:
        return auction_rooms[0]

@socket_io.on("emit_bid")
def handle_emit(data: Dict[str, Any]) -> None:
    room_id = get_room_id()
 
    value = data.get("value", None)
    product_id = data.get("product_id", None)
    product_name = data.get("product_name", None)

    missingInfo = [i for i in [room_id, value, product_id, product_name] if i == None]

    if missingInfo:
        response = {
            "type": "error",
            "Error": "Missing Information",
            "MissingInformation": missingInfo  
        }
        return emit("server_content", {"response":response}, to=request.sid)

    data = {
        "type": "bid",
        "room_id": room_id,
        "user_id": session.get("id"),
        "username": session.get("username") if not request.cookies.get("anonymous") else f"AnonymousUser{anonymous_users_number}",
        "value": value,
        "product_id": product_id,
        "product_name": product_name
    }

    out = make_bid(data)
    if (out):
        response = data
        return emit("server_content", {"response": {"type": "error", "Error":out}}, to=request.sid)

    return emit("server_content", {"response": response}, to=room_id)