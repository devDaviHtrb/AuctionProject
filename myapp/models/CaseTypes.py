from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class case_types(db.Model):
    case_type_id = db.Column(db.Integer, primary_key=True)
    case_type_name = db.Column(db.String(10), nullable=False)
