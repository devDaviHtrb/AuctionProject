from sqlalchemy.exc import SQLAlchemyError
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Products import products
from myapp.services.ProductService import add_time_to_auction
import myapp.repositories.BidRepository as bid_repository
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.UserRepository as user_repository
from typing import Tuple, Dict, Any
from decimal import Decimal

#===================================== ERRORS =====================================
MISSING_INFO =      101 # Missing Informations
INVALID_PRODUCT =   102 # Invalid Product
INSUFICIENT_FUNDS = 103 # Insuficient funds
BID_VALUE_ERROR =   104 # Bid must be higher than current highest bid
OTHER_BIDS_ERROR =  105 # The sum of all your bids exceeds your balance
PROCESS_ERROR =     106 # Error processing bid
WINNER_USER_BID =   107 # The winning bid and the current bid have the same users.
#==================================================================================

OCCURRING = "Ativo"
MINUTE =    60

def make_bid(user_id: int, product: products, value: int) -> Tuple[bool, Dict[str, Any]]:
    product_id = product.product_id
    try:
        if not product or product_repository.get_status(product) != OCCURRING:
            return False, INVALID_PRODUCT

        user = user_repository.get_by_id(user_id)
        if user.wallet < value:
            return False, INSUFICIENT_FUNDS

        last_bid = product_repository.get_last_bid(product)

        if last_bid and value <= last_bid.bid_value:
            return False, BID_VALUE_ERROR
        
        #BUSSINES RULES

        if(last_bid and last_bid.user_id == user_id):
            return False, WINNER_USER_BID


        active_bids = user_repository.get_winner_bids_with_restriction(user, product)

        t_sum = sum([current.bid_value for current in active_bids], Decimal('0'))
        if t_sum + Decimal(value) > user.wallet:
            return False, OTHER_BIDS_ERROR

        new_bid = bid_repository.save_item({
            "bid_value": value,
            "user_id": user_id,
            "product_id": product_id
        })

        product.min_bid = value

        db.session.commit()

        add_time_to_auction(product_id, MINUTE * 2)

        return True, new_bid

    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error:", e)
        return False, PROCESS_ERROR
