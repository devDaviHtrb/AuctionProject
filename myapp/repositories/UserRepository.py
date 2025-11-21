from myapp.models.Users import users
from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons
from myapp.models.Settings import settings
from myapp.models.Bids import bids
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
import myapp.repositories.SettingRepository as setting_repository
from werkzeug.security import generate_password_hash
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import func, and_
from typing import Optional, Tuple, Dict, Any, List

from myapp.utils.UploadImage import upload_image

def get_id(user:users) -> str:
    return str(user.user_id)

def get_type(user:users) -> str:
    return "legal_person" if (legal_persons.query.get(user.user_id)) else "physical_person"

def set_api_token(user:users, new_api_token:str) -> None:
    user.api_token = new_api_token
    db.session.commit()

def get_by_email(wanted_email:str) -> Optional[users]:
    return db.session.query(users).filter(
        users.email == wanted_email
    ).first()

def get_by_username(wanted_username: str) -> Optional[users]:
    return users.query.filter_by(username = wanted_username).first()

def get_by_id(wanted_id: int) -> Optional[users]:
    return users.query.get(wanted_id)

def get_two_factor_auth(user:users) -> Optional[bool]:
    setting = db.session.query(settings).filter_by(user_id = user.user_id).first()
    return setting.two_factor_auth if setting else None

def set_password(user:users, new_password: str) -> None:
    user.password = generate_password_hash(new_password)
    db.session.commit()

def delete(user:users) -> Tuple[bool, str]:
    try:
        db.session.delete(user)
        db.session.commit()
        return True, "ok"
    except Exception as e:
        db.session.rollback()
        return False, e

def save_item(data: Dict[str, Any]) -> users:
    user_type = data.get("userType", "physical_person")
    user = users(
        username = data.get("username"),
        password = generate_password_hash(data.get("password")),
        email = data.get("email"),
        cpf = data.get("cpf"),
        name = data.get("name"),
        photo = data.get("photo_url", None),
        cellphone1 = data.get("cellphone1", None),
        cellphone2 = data.get("cellphone2", None),
        landline = data.get("landline", None),
        wallet = 100, #rs
        active_auction_number = float(0),
        password_token_expiration_datetime = None,
        api_token = None,
        password_token = None,
        admin_user = False,
    )
    db.session.add(user)
    db.session.flush() #generate the user id
    
    """
    create_adress(
        street_name = data.get("street_name"),
        street_number = data.get("street_number"),
        apt = data.get("apt", None),
        zip_code = data.get("zip_code"),
        district = data.get("district"),
        city = data.get("city"),
        state = data.get("state")),
        principal_adress = True,
        user_id = user.user_id
    """

    if user_type == "physical_person":
        physical_person = physical_persons(
            user_id = user.user_id, 
            rg = data.get("rg"), 
            birth_date = data.get("birth_date"), 
            gender = data.get("gender")
        )
        db.session.add(physical_person)
    else:  # legal person
        legal_person = legal_persons(
            user_id = user.user_id,
            scrap_purchase_authorization = data.get("scrap_purchase_authorization", False),
            trade_name = data.get("trade_name"), 
            legal_business_name = data.get("legal_business_name"),
            cnpj = data.get("cnpj"),
            state_tax_registration = data.get("state_tax_registration")
        )
        db.session.add(legal_person)
    
    setting_repository.save_item(user.user_id)
    
    db.session.commit()
    return user

def delete_bids_by_product_id_user_id(user_id:int, product_id:int) -> None:
    stmt = delete(bids).where(
        bids.product_id == product_id,
        bids.user_id == user_id
    )
    db.session.execute(stmt)
    db.session.commit()

def get_by_api_token(wanted_token:str) -> Optional[users]:
    return users.query.filter_by(api_token = wanted_token).first()

# differents of product_id(parameter)
def get_winner_bids_with_restriction(user:users, product:products) -> List[bids]:
    subquery = (
        db.session.query(
            bids.product_id,
            func.max(bids.bid_value).label('max_value')
        ).group_by(bids.product_id).subquery()
    )

    return (
        db.session.query(bids).join(
            subquery, and_(
            bids.product_id == subquery.c.product_id,
            bids.bid_value == subquery.c.max_value
            )
        ).join(
            products,
            bids.product_id == products.product_id
        ).join(
            product_statuses,
            product_statuses.product_status_id == products.product_status
        ).filter(
            product_statuses.product_status_id == product.product_status,
            bids.product_id != product.product_id,
            bids.user_id == user.user_id, 
        )
    )


def force_logout_all():
    users.query.filter_by(admin_user=False).update({ "force_logout": True })
    db.session.commit()


def force_logout_user(username):
    users.query.filter_by(username=username, admin_user=False).update({ "force_logout": True })
    db.session.commit()
