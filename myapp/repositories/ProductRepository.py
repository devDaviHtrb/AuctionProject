from myapp.models.ProductStatuses import product_statuses
from myapp.models.Categories import categories
from myapp.models.TechnicalFeatures import technical_features
from myapp.models.CategoryTechnicalFeatures import category_technical_features
from myapp.models.Products import products
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Images import images
from myapp.setup.InitSqlAlchemy import db
import myapp.repositories.AddressRepository as address_repository
import myapp.repositories.BidRepository as bids_repository
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select

from myapp.utils.UploadImage import upload_image

def save_item(data: Dict[str, Any], legal_data:Optional[Dict[str, Any]] = None) -> products:
    if data.get("product_status"):
        data["product_status"] = db.session.execute(
            select(product_statuses.product_status_id)
            .where(product_statuses.product_status == data["product_status"])
        ).scalar()

    if data.get("category"):
        data["category"] = db.session.execute(
            select(categories.category_id)
            .where(categories.category_name == data["category"])
        ).scalar()
    product_imgs = upload_image(data["photos"], "Users_photos")
    
    if product_imgs:
        data["photos_url"] = product_imgs
    else:
        print("Db connection error")
    new_product = products(**data)
    db.session.add(new_product)
    db.session.flush()  # cria o product_id

    if data.get("photos_url"):
        for url in data["photos_url"]:
            new_product_img = images(
                image=url,
                principal_image=True if data["photos_url"].index(url) == 0 else False,
                product_id=new_product.product_id
        )
            db.session.add(new_product_img)

    db.session.commit()

    if (legal_data):
        legal_data["product_id"] = new_product.product_id
        address_repository.save_item(legal_data)

    return new_product

def get_user(product:products) -> users:
    return users.query.get(product.user_id)

def get_status(product:products) -> str:
    stmt = select(product_statuses).where(
        product_statuses.product_status_id == product.product_status
    )
    result = db.session.execute(stmt).scalar()
    return result.product_status  # integrity never return None

def set_status(product:products, new_status: str) -> None:
    new_fk = db.session.execute(
        select(product_statuses.product_status_id)
        .where(product_statuses.product_status == new_status.lower())
    ).scalar()

    if new_fk:
        product.product_status = new_fk
        db.session.commit()

def get_actives() -> List[products]:
    query = db.session.query(products).join(
        product_statuses,
        products.product_status == product_statuses.product_status_id
    ).filter(
        product_statuses.product_status == "active"
    )

    return query.all()

def get_technical_feature_id(product:products) -> List[technical_features]:
    return technical_features.query.join(
        category_technical_features,
        category_technical_features.technical_feature_id == technical_features.technical_feature_id
    ).filter(
        product.category == category_technical_features.category_id
    ).all()

def last_bid(product:products, chunk_size:int = 10) -> Optional[Tuple[bids, users]]:
    offset = 0
    while True:
        consulted_bids = bids.get_bids_filter(
            product_id = product.product_id,
            offset = offset,
            chunk_size = chunk_size
        )

        if not consulted_bids:
            return

        for bid in consulted_bids:
            bid_user = bids_repository.is_valid(bid)
            if(bid_user):
                return bid, bid_user