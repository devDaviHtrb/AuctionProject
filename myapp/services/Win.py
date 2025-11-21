from myapp.models.Products import products
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.PaymentRepository as payment_repository
from myapp.setup.InitSqlAlchemy import db, get_session
from datetime import datetime
from typing import List, Optional

INTERN_MONEY =  "intern_money"
RECEIVED =      "received"

def set_winner(product: products, ignores:Optional[List[int]]=None) -> None:
    if ignores is None:
        ignores = []

    while True:

        winner_bid, winner_user = product_repository.last_bid(
            product=product,
            ignores_ids=ignores,
            chunk_size=10
        )

        if not winner_bid or not winner_user:
            return

        print(winner_bid.user_id, flush=True)

        session = get_session()

        try:
            seller_user = product_repository.get_user(product, session=session)
            bid_value = winner_bid.bid_value

            winner_user.wallet -= bid_value
            seller_user.wallet += bid_value
            winner_bid.winner = True

            session.add(winner_user)
            session.add(seller_user)
            session.add(winner_bid)

            data = {
                "amount": bid_value,
                "confirmation_datetime": datetime.utcnow(),
                "payer_user_id": seller_user.user_id,
                "payee_user_id": winner_user.user_id,
                "payment_method": INTERN_MONEY,
                "payment_status": RECEIVED
            }

            payment_repository.save_item(data, session=session)

            session.commit()

        except Exception as e:
            session.rollback()
            print("Error:", e, flush=True)
            ignores.append(winner_bid.bid_id)

        finally:
            session.close()
