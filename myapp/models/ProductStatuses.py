from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class product_statuses(db.Model):
    product_status_id = db.Column(db.Integer, primary_key=True)
    payment_status = db.Column(db.String(20), nullable=False)
