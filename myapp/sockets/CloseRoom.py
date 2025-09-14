import threading as thread
from datetime import datetime, timedelta
from myapp.setup.InitSocket import socket_io
#from myapp.setup.InitSqlAlchemy import db
#from myapp.models.Auction import Auction

auction_timers = {}      # {auction_id, thread.Timer}

def close_auction(auction_id:int) -> None:
    '''
    delete in Database
    verify if auction status is != closed
    verify the winner
    #cmp
    '''
    # auction = db.query(Auction).get(auction_id)

    cmp = True
    if (cmp): # if(auction and auction.status != "closed")
        """
        set as closed
        """
        #acution.status = "closed"
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

        auction_timers.pop(auction_id)

def restart() -> None:
    # active_auctions = auctions that are active
    # for auction in active_auctions:
    #   delta = auction.end() - datetime.utcnow()
    #   if delta < 0:
    #       close_auction(auction.id)
    #   else:
    #       start_auction_timer(auction.id, delta.total_seconds())  
    pass

def add_time_to_auction(auction_id: int, seconds:int) -> None:
    if auction_id not in auction_timers:
        return 
    
    auction_timers[auction_timers].cancel()
    # auction = db.query(Auction).get(auction_id)
    # acution.end += timedelta(seconds = seconds)
    # remaining_seconds = (auction.end - datetime.utcnow()).total_seconds()
    ##total_seconds is for timedelta class
    # if remaining_seconds < 0:
    #   return
    # timer = thread.Timer(remaining_seconds, close_auction, args=[auction_id])
    # timer.start()
    # auction_timers[auction_id] = timer

def start_auction_timer(auction_id:int, seconds:int) -> None:
    end_time = datetime.now() + timedelta(seconds=seconds)
    # auction = db.query(Auction).get(auction_id)
    # acutin.end = end_time
    timer = thread.Timer(seconds, close_auction, args=[auction_id])
    timer.start()
    auction_timers[auction_timers] = timer
