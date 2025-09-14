from flask_socketio import emit, join_room
from typing import Dict, Any
from myapp.setup.InitSocket import socket_io

@socket_io.on("join_room")
def handle_join(data: Dict[str, Any]) -> None:
    room_id = data["room_id"]
    join_room(room_id)
    response = {
        "type": "entry",
        "room_id": room_id,
        "user_id": data.get("user_id"),
        "username": data.get("username"),
        "product_id": data.get("product_id"),
        "product_name": data.get("product_name")
    }
    emit("server_content", {"response": response}, to=room_id)


@socket_io.on("bid_content")
def handle_content(data: Dict[str, Any]) -> None:
    room_id = data.get("to_room_id")
    user_id = data.get("user_id"),
    username = data.get("username")
    value = data.get("value")
    product_id = data.get("product_id")
    product_name = data.get("product_name")

    response = {
        "type": "bid",
        "room_id": room_id,
        "user_id": user_id,
        "username": username,
        "value": value,
        "product_id": product_id,
        "product_name": product_name
    }

    if room_id:
        emit("server_content", {"response": response}, to=room_id)