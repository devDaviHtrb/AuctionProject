from myapp.setup.InitSqlAlchemy import db
from myapp.models.Settings import settings

def save_item(user_id:int) -> settings:
    new_setting = settings(user_id = user_id)
    db.session.add(new_setting)
    db.session.flush()
    db.session.commit()

    return new_setting