from myapp.models.ProductStatuses import product_statuses
from myapp.models.Categories import categories
from myapp.models.TechnicalFeatures import technical_features
from myapp.models.Products import products
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Images import images
from myapp.models.TechnicalFeaturesValues import technical_features_values
from myapp.models.LegalInfos import legal_infos
from myapp.setup.InitCache import cached
from myapp.setup.InitSqlAlchemy import db
import myapp.repositories.LegalInfosRepository as legal_info_repository
import myapp.repositories.BidRepository as bids_repository
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from myapp.utils.UploadImage import upload_image

CANCELED =          "Suspenso"
FINISHED =          "Finalizado" 
OCCURRING =         "Ativo"
NOT_OCCURRING  =    "Nao_Iniciado"


def save_item(data: Dict[str, Any], legal_data:Optional[Dict[str, Any]] = None) -> products:
    if data.get("product_status"):
        data["product_status"] = db.session.execute(
            select(product_statuses.product_status_id)
            .where(product_statuses.product_status == NOT_OCCURRING)
        ).scalar()

    if data.get("category"):
        data["category"] = db.session.execute(
            select(categories.category_id)
            .where(categories.category_name == data["category"])
        ).scalar()
    valid_files = [f for f in data.get("photos", list()) if f and f.filename]
    product_imgs = upload_image(valid_files, "Users_photos")
    
    print(data, flush=True)
    data.pop("photos")
    data["first_value"] = data["min_bid"]
    new_product = products(**data)
    db.session.add(new_product)
    db.session.flush() 

    photos_url = []
    if product_imgs:
        photos_url = product_imgs
    else:
        print("Db connection error")
    for url in photos_url:
        new_product_img = images(
            image=url,
            principal_image=True if photos_url.index(url) == 0 else False,
            product_id=new_product.product_id
        )
        db.session.add(new_product_img)

    db.session.commit()

    if (legal_data):
        legal_data["product_id"] = new_product.product_id
        legal_info_repository.save_item(legal_data)

    return new_product


def get_user(product:products, session:Optional[sessionmaker] = None) -> users:
    if (sessionmaker is None):
        return users.query.get(product.user_id)
    return session.query(users).get(product.user_id)

def get_status(product:products) -> str:
    stmt = select(product_statuses).where(
        product_statuses.product_status_id == product.product_status
    )
    result = db.session.execute(stmt).scalar()
    return result.product_status  # integrity never return None

def set_status(product:products, new_status: str) -> None:
    new_fk = db.session.execute(
        select(product_statuses.product_status_id)
        .where(product_statuses.product_status == new_status)
    ).scalar()

    if new_fk:
        product.product_status = new_fk
        db.session.commit()

@cached(timeout=600)
def get_actives() -> List[products]:
    query = db.session.query(products).join(
        product_statuses,
        products.product_status == product_statuses.product_status_id
    ).filter(
        product_statuses.product_status == OCCURRING
    )

    return query.all()

@cached(timeout=600)
def get_inactives() -> List[products]:
    query = db.session.query(products).join(
        product_statuses,
        products.product_status == product_statuses.product_status_id
    ).filter(
        product_statuses.product_status == NOT_OCCURRING
    )

    return query.all()

def last_bid(product:products, ignores_ids:List[int], chunk_size:int = 10) -> Optional[Tuple[bids, users]]:
    offset = 0
    while True:
        consulted_bids = bids_repository.get_bids_filter(
            product_id = product.product_id,
            offset = offset,
            chunk_size = chunk_size
        )

        if not consulted_bids:
            return (None, None)

        for bid in consulted_bids:
            bid_user = bids_repository.is_valid(bid, ignores_ids)
            if(bid_user):
                return bid, bid_user
        offset += chunk_size

@cached(timeout=600)
def get_technical_features_name_and_values(product: products):
    results = (
        db.session.query(
            technical_features.technical_feature_name,
            technical_features_values.value
        )
        .join(
            technical_features,
            technical_features_values.technical_feature_id == technical_features.technical_feature_id,
            isouter=True
        )
        .filter(
            technical_features_values.product_id == product.product_id
        )
        .all()
    )

    return results


@cached(timeout=600)
def get_room_id_by_id(wanted_id:int) -> Optional[str]:
    return db.session.execute(
        select(products.product_room).where(
            products.product_id == wanted_id
        )
    ).scalar()


def get_a_and_status_by_room_id(wanted_room_id:str) -> Optional[products]:
    return products.query.join(
        product_statuses,
        product_statuses.product_status_id == products.product_status,
        isouter = True
    ).filter(products.product_room == wanted_room_id).first()

@cached(timeout=600)
def get_images(product: products) -> List[images]:
    return images.query.filter_by(product_id = product.product_id).all()

#get the join of product, images and status of differents actives products order by room_id(random)
@cached(timeout=300)
def get_and_images_and_status_diffents_valids_randomly(
    product:products,
    limit:int = 3
) -> List[products]:
    return products.query(
        products.product_name,
        products.product_room,
        products.min_bid,
        products.start_datetime,
        products.duration,
        images.image
    ).join(
        images,
        images.product_id == products.product_id,
        isouter = True
    ).join(
        product_statuses,
        product_statuses.product_status_id == products.product_status,
        isouter=True
    ).order_by(
        products.product_room
    ).filter(
        products.product_room != product.product_room,
        product_statuses.product_status != CANCELED,
        product_statuses.product_status != FINISHED
    ).distinct().limit(limit).all()

def get_value_datetime_username_of_last_bids(product:products) -> Optional[bids]:
    return (
        db.session.query(
            bids.bid_value, bids.bid_datetime, users.username
        ).join(
            users, bids.user_id == users.user_id
        ).filter(
            bids.product_id == product.product_id
        ).order_by(bids.bid_value.desc())
    )

@cached(timeout=600)
def get_category(product:products) -> str:
    return categories.query.get(product.category).category_name

@cached(timeout=600)
def get_legal_info(product:products) -> str:
    legal_infos.query.filter_by(product_id = product.product_id).first()

def get_by_id(wanted_id:int) -> Optional[products]:
    return products.query.get(wanted_id)

def get_by_room_id(wanted_room_id:int ) -> Optional[products]:
    return products.query.filter_by(product_room = wanted_room_id).first()

def get_last_bid(product:products) -> Optional[bids]:
    return (
            db.session.query(bids)
            .filter_by(product_id=product.product_id)
            .order_by(bids.bid_value.desc())
            .with_for_update()
            .first()
        )

def get_bids_by_user(user:users) -> List[products]:
    return products.query.filter_by(user_id = user.user_id).all()