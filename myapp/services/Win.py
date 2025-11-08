from myapp.models.Products import products
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.PaymentRepository as payment_repository
from myapp.setup.InitSqlAlchemy import db
from datetime import datetime
from typing import List, Optional

INTERN_MONEY =  "intern_money"
RECEIVED =      "received"

def set_winner(product: products, ignores:Optional[List[int]]=None) -> None:
    if ignores is None:
        ignores = []
    while(True):
        winner_bid, winner_user = product_repository.last_bid(
            product,
            chunk_size=10,
            ignores = ignores
        )
        try:
            with db.session.begin(): 
                if not winner_bid or not winner_user:
                    return

                seller_user = product_repository.get_user(product)
                bid_value = winner_bid.bid_value

                winner_user.wallet -= bid_value
                seller_user.wallet += bid_value
                winner_bid.winner = True

            
                product.user_id = winner_user.user_id

                
                data = {
                    "amount": bid_value,
                    "confirmation_datetime":    datetime.utcnow(),
                    "payer_user_id":            seller_user.user_id,
                    "payee_user_id":            winner_user.user_id,
                    "payment_method":           INTERN_MONEY,
                    "payment_status":           RECEIVED
                }

                
                payment_repository.save_item(data)


        except Exception as e:
            db.session.rollback()
            ignores.append(winner_bid.bid_id)
        
