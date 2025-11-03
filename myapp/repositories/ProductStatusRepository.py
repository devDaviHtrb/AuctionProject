from myapp.models.ProductStatuses import product_statuses
from myapp.models.Products import products
from sqlalchemy import func
from typing import List, Tuple

def get_status_frequencies() -> List[Tuple[str, int]]:
    results = (
        product_statuses.query
        .outerjoin(products, products.product_status == product_statuses.product_status_id)
        .with_entities(product_statuses.product_status, func.count(products.product_id))
        .group_by(product_statuses.product_status)
        .all()
    )

    return results