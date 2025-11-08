from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class addresses(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(6), nullable=False)
    apt = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.CHAR(9), nullable=False)
    district = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.CHAR(2), nullable=False)
    principal_address = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
