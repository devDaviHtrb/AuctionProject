import threading as thread
from datetime import datetime, timedelta
from myapp.setup.InitSocket import socket_io
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses

products_timers = {}      # {auction_id, thread.Timer}

def close_auction(product_id:int) -> None:
    '''
    delete in Database
    verify if auction status is != closed
    verify the winner
    #cmp
    '''
    product = products.query.get(product_id)

    status = product.get_status().upper() == "OCCURRING"
    if (product and status): 
        """
        set as closed
        """
        #acution.status = "closed"
        room_id = product_id #pesquisa
        # win
        socket_io.emit(
            "auctin_closed",
            {
                "product_id": product_id,
                "message": "Finish Auction",
            },
            room = room_id
        )

        if room_id in socket_io.server.manager.rooms["/"]:
            clients = list(socket_io.server.manager.rooms["/"][room_id])
            for client in clients:
                socket_io.leave_room(client, room_id)

        products_timers.pop(product_id)

def restart() -> None:
    active_products = products.get_actives()
    products_timers.clear()
    for product in active_products:
        delta = product.end() - datetime.utcnow()
        if delta < 0:
            close_auction(product.product_id)
        else:
            start_auction_timer(product.product_id, delta.total_seconds())  


def add_time_to_auction(product_id: int, seconds:int) -> None:
    if product_id not in products_timers:
        return 
    
    products_timers[product_id].cancel()
    product = products.query.get(product_id)
    product.end_datetime += timedelta(seconds = seconds)

    #obs ->>>>
    remaining_seconds = (product.end_datetime.end - datetime.utcnow()).total_seconds()
    ##total_seconds is for timedelta class
    if remaining_seconds < 0:
       return
    timer = thread.Timer(remaining_seconds, close_auction, args=[product_id])
    timer.start()
    products_timers[product_id] = timer

def start_auction_timer(product_id:int, seconds:int) -> None:
    end_time = datetime.now() + timedelta(seconds=seconds)
    product = products.query.get(product_id).first()
    product.end = end_time
    timer = thread.Timer(seconds, close_auction, args=[product_id])
    timer.start()
    products_timers[product_id] = timer
