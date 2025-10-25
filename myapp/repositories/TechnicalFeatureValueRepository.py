from myapp.models.TechnicalFeaturesValues import technical_features_values
from myapp.setup.InitSqlAlchemy import db

def save_item(data) -> technical_features_values:
    ntfv = technical_features_values(**data)
    db.session.add(ntfv)
    db.session.flush()
    db.session.commit()

    return ntfv