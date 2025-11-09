import threading as thread
from datetime import datetime, timedelta
from myapp.setup.InitSocket import socket_io
from myapp.services.Win import set_winner
import myapp.repositories.ProductRepository as product_repository
from myapp.sockets.Room import last_emit_times

#============= TIMER =============
#{
#   product_id: {
#        "timer": thread.Timer,
#        "end_datetime": datetime
#    }
#}
#=================================
products_timers = {}

OCCURRING = "Ativo"

def close_auction(product_id: int) -> None:
    product = product_repository.get_by_id(product_id)

    if not product:
        return

    status = product_repository.get_status(product).lower() == OCCURRING
    if (status):
        room_id = product_id
        socket_io.emit(
            "auction_closed",
            {
                "product_id": product_id,
                "message": "Finish Auction"
            },
            room=room_id
        )

        if room_id in socket_io.server.manager.rooms["/"]:
            clients = list(socket_io.server.manager.rooms["/"][room_id])
            for client in clients:
                socket_io.leave_room(client, room_id)

        set_winner(product)
        product.end_datetime = products_timers[product_id]["end_datetime"]
        product_repository.set_status(product, "finished")
        products_timers.pop(product_id, None)

        last_emit_times.pop(room_id, None)


def start_auction_timer(product_id: int, seconds: int) -> None:
    end_time = datetime.utcnow() + timedelta(seconds=seconds)
    timer = thread.Timer(seconds, close_auction, args=[product_id])
    timer.start()

    products_timers[product_id] = {
        "timer": timer,
        "end_datetime": end_time
    }


def restart() -> None:
    active_products = product_repository.get_actives()
    products_timers.clear()

    for product in active_products:
        remaining_seconds = max(
            product.start_datetime + timedelta(seconds=product.duration) - datetime.utcnow(),
            timedelta(seconds=60*10),
        ).total_seconds()
        
        start_auction_timer(product.product_id, remaining_seconds)


def add_time_to_auction(product_id: int, seconds: int) -> None:
    if product_id not in products_timers:
        return

    products_timers[product_id]["timer"].cancel()

    products_timers[product_id]["end_datetime"] += timedelta(seconds=seconds)


    remaining_seconds = (
        products_timers[product_id]["end_datetime"] - datetime.utcnow()
    ).total_seconds()

    if remaining_seconds <= 0:
        close_auction(product_id)
        return

    timer = thread.Timer(remaining_seconds, close_auction, args=[product_id])
    timer.start()
    products_timers[product_id]["timer"] = timer
