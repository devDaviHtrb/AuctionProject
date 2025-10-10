from flask_socketio import emit, join_room, rooms
from typing import Dict, Any
from myapp.setup.InitSocket import socket_io
from flask import request
from flask_login import current_user

anonymous_users_number = 0

@socket_io.on("join_room")
def handle_join(data: Dict[str, Any]) -> None:
    room_id = data["room_id"]
    if (None in [room_id, current_user.user_id]):
        return
    join_room(room_id)
    response = {
        "type": "entry",
        "room_id": room_id,
        "user_id": current_user.user_id,
        "username": current_user.username if not request.cookies.get("anonymous") else f"AnonymousUser{anonymous_users_number}",
    }
    anonymous_users_number+=1
    emit("server_content", {"response": response}, to=room_id)


@socket_io.on("emit_bid")
def handle_content(data: Dict[str, Any]) -> None:
    auction_rooms = [r for r in rooms() if r != request.sid]
    room_id = auction_rooms[0] if auction_rooms else None
 
    value = data.get("value", None)
    product_id = data.get("product_id", None)
    product_name = data.get("product_name", None)

    if None in [room_id, value, product_id, product_name]:
        return
    
    """if not bid():
        return """
    response = {
        "type": "bid",
        "room_id": room_id,
        "user_id": current_user.user_id,
        "username": current_user.username if not request.cookies.get("anonymous") else f"AnonymousUser{anonymous_users_number}",
        "value": value,
        "product_id": product_id,
        "product_name": product_name
    }

    if room_id:
        emit("server_content", {"response": response}, to=room_id)