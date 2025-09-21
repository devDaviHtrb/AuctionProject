from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class payment_methods(db.Model):
    payment_method_id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(20), nullable=False)
