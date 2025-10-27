from myapp.models.Addresses import addresses
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any

def save_item(data:Dict[str, Any]) -> addresses:
    new_address = addresses(**data)
    db.session.add(new_address)
    db.session.flush()
    db.session.commit()
    return new_address