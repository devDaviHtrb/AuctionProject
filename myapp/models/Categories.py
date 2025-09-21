from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80), nullable=False)
