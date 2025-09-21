from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class products(db.Model):
    product_id =  db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    despription =  db.Column(db.Text, nullable=True)
    min_bid = db.Column(db.DECIMAL(12, 2), nullable=True)
    start_datetime =  db.Column(db.DateTime, nullable=True)
    product_status=db.Column(db.SmallInteger, nullable=True)
    street_name = db.Column(db.String(255), nullable=True)
    street_number = db.Column(db.String(6), nullable=True)
    apt = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.CHAR(9), nullable=True)
    district = db.Column(db.String(80), nullable=True)
    city =db.Column(db.String(80), nullable=True)
    state =db.Column(db.CHAR(2), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
    category_id = db.Column(db.Integer, ForeignKey("categories.category_id"))