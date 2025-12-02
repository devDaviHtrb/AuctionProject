from myapp.models.Categories import categories
from myapp.models.CategoryTechnicalFeatures import category_technical_features
from myapp.models.TechnicalFeatures import technical_features
from myapp.models.CaseTypes import case_types
from myapp.models.PaymentStatuses import payment_statuses
from myapp.models.PaymentMethods import payment_methods
from myapp.setup.InitSqlAlchemy import db
import myapp.setup.Inserts as inserts

#
def payment_statuses_inserts() -> None:
    for data in inserts.payment_statuses_data:
        db.session.add(payment_statuses(**data))
    db.session.commit()

#
def payment_methods_inserts() -> None:
    for data in inserts.payment_methods_data:
        db.session.add(payment_methods(**data))
    db.session.commit()

#
def case_types_inserts() -> None:
    for data in inserts.case_types_data:
        db.session.add(case_types(**data))
    db.session.commit()

#
def categories_inserts() -> None:
    for data in inserts.categories_data:
        db.session.add(categories(**data))
    db.session.commit()

#
def technical_features_inserts() -> None:
    for data in inserts.technical_features_data:
        db.session.add(technical_features(**data))
    db.session.commit()

def category_technical_features_inserts() -> None:
    for data in inserts.category_technical_features_data:
        db.session.add(category_technical_features(**data))
    db.session.commit()


def all_inserts() -> None:
    if(payment_statuses.query.first() is None):
        payment_statuses_inserts()
    
    if(payment_methods.query.first() is None):
        payment_methods_inserts()
    
    if(case_types.query.first() is None):
        case_types_inserts()

    if(categories.query.first() is None):
        categories_inserts()

    if(technical_features.query.first() is None):
        technical_features_inserts()
    
    if(category_technical_features.query.first() is None):
        category_technical_features_inserts()