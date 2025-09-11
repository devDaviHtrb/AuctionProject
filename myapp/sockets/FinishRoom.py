import threading as thread
from datetime import datetime, timedelta
from myapp.setup.InitSocket import socket_io

def close_auction(auction_id:int) -> None:
    '''
    delete in Database
    verify if auction status is != closed
    #cmp
    '''
    cmp = True
    if (cmp):
        """
        set as closed
        """
        room_id = auction_id #pesquisa
        socket_io.emit(
            "auctin_closed",
            {
                "auction_id": auction_id,
                "message": "Fish Auction",
            },
            room = room_id
        )

        if room_id in socket_io.server.manager.rooms["/"]:
            clients = list(socket_io.server.manager.rooms["/"][room_id])
            for client in clients:
                socket_io.leave_room(client, room_id)


def acution_timer(auction_id:int, minutes:int) -> None:
    timer = thread.Timer(minutes*60, close_auction, args=[auction_id])
    timer.start()
