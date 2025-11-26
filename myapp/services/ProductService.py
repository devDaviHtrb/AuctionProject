from flask import current_app
import threading
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from myapp.setup.InitSocket import socket_io
from myapp.services.Win import set_winner
import myapp.repositories.ProductRepository as product_repository

products_timers_close = {}
products_timers_open = {}

OCCURRING = "Ativo"
FINISHED =  "Finalizado"

def open_auction(product_id: int) -> None:
    app = current_app._get_current_object()
    with app.app_context():
        product = product_repository.get_by_id(product_id)
        if not product:
            return

        product_repository.set_status(product, OCCURRING)

        if not product.start_datetime:
            return

        now = datetime.now(ZoneInfo("UTC"))
        end_dt = product.start_datetime + timedelta(minutes=product.duration)
        remaining = (end_dt - now).total_seconds()

        if remaining <= 0:
            print(f"[OPEN] Auction {product_id} opened late; skip scheduling close.", flush=True)
            return

        start_close_timer(product_id, int(remaining))
        print(f"[OPEN] Auction {product_id} opened.", flush=True)


def start_open_timer(product_id: int, seconds: int) -> None:
    if(seconds <= 0):
        open_auction(product_id)
        return
    app = current_app._get_current_object()

    def callback():
        with app.app_context():
            open_auction(product_id)

    timer = threading.Timer(seconds, callback)
    timer.daemon = True
    timer.start()

    products_timers_open[product_id] = {
        "timer": timer,
        "end_datetime": datetime.now(ZoneInfo("UTC")) + timedelta(seconds=seconds)
    }


def restart_open() -> None:
    app = current_app._get_current_object()
    with app.app_context():
        inactive_products = product_repository.get_inactives()
        products_timers_open.clear()
        now = datetime.now(ZoneInfo("UTC"))
        if inactive_products:
            for product in inactive_products:
                if not product.start_datetime:
                    continue

                remaining = (product.start_datetime - now).total_seconds()

                if remaining <= 0:
                    print(f"[RESTART_OPEN] Auction {product.product_id} should already be open.", flush=True)
                    print(f"NOW IS: {now} & STARTDATETIME: {product.start_datetime}")
                    open_auction(product.product_id)
                    continue

            start_open_timer(product.product_id, int(remaining))
            print(f"[RESTART_OPEN] Scheduled opening for {product.product_id}.", flush=True)


def close_auction(product_id: int) -> None:
    app = current_app._get_current_object()
    with app.app_context():
        product = product_repository.get_by_id(product_id)
        if not product:
            products_timers_close.pop(product_id, None)
            return

        status = product_repository.get_status(product)
        if status.lower() != OCCURRING.lower():
            products_timers_close.pop(product_id, None)
            return

        room_id = product.product_room

        rooms = socket_io.server.manager.rooms.get("/", {})
        if room_id in rooms:
            for client in list(rooms[room_id]):
                socket_io.server.leave_room(client, room_id, namespace="/")

        set_winner(product)

        timer_info = products_timers_close.get(product_id)
        if timer_info:
            product.end_datetime = timer_info["end_datetime"]

        product_repository.set_status(product, FINISHED)

        products_timers_close.pop(product_id, None)

    print(f"[CLOSE] Auction {product_id} closed.", flush=True)



def start_close_timer(product_id: int, seconds: int) -> None:
    if(seconds <= 0):
        close_auction(product_id)
        return
    app = current_app._get_current_object()

    def callback():
        with app.app_context():
            close_auction(product_id)

    timer = threading.Timer(seconds, callback)
    timer.daemon = True
    timer.start()

    products_timers_close[product_id] = {
        "timer": timer,
        "end_datetime": datetime.now(ZoneInfo("UTC")) + timedelta(seconds=seconds)
    }


def restart_closes() -> None:
    print()
    app = current_app._get_current_object()
    with app.app_context():
        active_products = product_repository.get_actives()
        products_timers_close.clear()
        now = datetime.now(ZoneInfo("UTC"))
        if active_products:
            for product in active_products:
                if not product.start_datetime:
                    continue

                end_dt = product.start_datetime + timedelta(minutes=product.duration)
                remaining = (end_dt - now).total_seconds()

                if remaining <= 0:
                    close_auction(product.product_id)
                    continue

            start_close_timer(product.product_id, int(remaining))
            print(remaining, now, product.start_datetime, flush=True)
            print(f"[RESTART_CLOSE] Scheduled close for {product.product_id}.", flush=True)


def add_time_to_auction(product_id: int, seconds: int) -> None:
    app = current_app._get_current_object()
    with app.app_context():
        if product_id not in products_timers_close:
            return

        timer_info = products_timers_close[product_id]

        
        timer_info["timer"].cancel()
        
        remaining = timer_info["end_datetime"] - datetime.now(ZoneInfo("UTC"))

        if (remaining <= timedelta(seconds=seconds)):
            timer_info["end_datetime"] += timedelta(seconds=seconds) - remaining

        now = datetime.now(ZoneInfo("UTC"))
        remaining = (timer_info["end_datetime"] - now).total_seconds()

        if remaining <= 0:
            close_auction(product_id)
            return

        start_close_timer(product_id, int(remaining))
