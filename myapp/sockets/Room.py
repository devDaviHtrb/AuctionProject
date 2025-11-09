from flask_socketio import emit, join_room, rooms
from typing import Dict, Any, List, Optional
from myapp.setup.InitSocket import socket_io
import myapp.repositories.ProductRepository as product_repository
from myapp.services.BidService import make_bid
from flask import request, session
from datetime import datetime, timedelta

anonymous_users_number = 0

#=============================== ERRORS ===============================
MISSING_INFO =      101 # Missing Informations
INVALID_PRODUCT =   102 # Invalid Product
INSUFICIENT_FUNDS = 103 # Insuficient funds
BID_VALUE_ERROR =   104 # Bid must be higher than current highest bid
OTHER_BIDS_ERROR =  105 # The sum of all your bids exceeds your balance
PROCESS_ERROR =     106 # Error processing bid
#======================================================================

OCCURRING = "Ativo"

last_emit_times: dict[str, Dict[int, datetime]] = {}

@socket_io.on("join_room")
def handle_join(data: Dict[str, Any]) -> None:
    print(data)
    room_id =   data.get("room_id", None)
    user_id =   session.get("user_id", None)
    username =  session.get("username", None)
    if (None in [room_id, user_id]):
        return
    product = product_repository.get_by_room_id(room_id)
    if(not product):
        return
    if(product_repository.get_status(product) != OCCURRING):
        return
    
    join_room(room_id)
    response = {
        "type":     "entry",
        "room_id":  room_id,
        "username": username if not request.cookies.get("anonymous", None) else f"AnonymousUser",
    }

    if(not room_id in last_emit_times ):
        last_emit_times[room_id] = {user_id : datetime.utcnow()}
    elif(not user_id in last_emit_times[room_id]):
        last_emit_times[room_id][user_id] = datetime.utcnow()
    elif(datetime.utcnow - last_emit_times[room_id][user_id] > timedelta(minutes=5)):
        last_emit_times[room_id][user_id] = datetime.utcnow()
    else:
        return
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
 
    user_id =   session.get("user_id", None)
    username =  session.get("username", None)

    value = max(float(data.get("value", 0)), 0)
    product = product_repository.get_by_room_id(room_id)
    print(data)

    missingInfo = [k for k, v in [("room_id", room_id), ("value", value), ("product", product)] if v is None]

    if missingInfo:
        print(missingInfo)
        response = {
            "type": "error",
            "error": MISSING_INFO,
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