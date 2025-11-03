from myapp.models.Categories import categories
from myapp.models.Products import products
from myapp.models.TechnicalFeatures import technical_features
from myapp.models.CategoryTechnicalFeatures import category_technical_features
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import select, func
from typing import List, Dict, Any

def get_all_name_id() -> List[Dict[str, Any]]:
    results = db.session.execute(
        select(categories.category_name, categories.category_id)
    ).all()
    
    return [(c_name, c_id, ) for c_name, c_id in results]

def get_technical_feature_id(category_id:int) -> List[technical_features]:
    return technical_features.query.join(
        category_technical_features,
        category_technical_features.technical_feature_id == technical_features.technical_feature_id
    ).filter(
        category_id == category_technical_features.category_id
    ).all()

def get_relationship_categories_features() -> Dict[categories, List[technical_features]]:
    all_categories = get_all_name_id()
    return {
        category_name: get_technical_feature_id(category_id)
        for category_name, category_id in all_categories
    } 

def get_categories_frequency():
    results = (
        categories.query
        .outerjoin(products, products.category == categories.category_id)
        .with_entities(categories.category_name, func.count(products.product_id))
        .group_by(categories.category_name)
        .all()
    )

    return results