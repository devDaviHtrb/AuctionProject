from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class images(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    principal_image = db.Column(db.Boolean, nullable=False)
    product_id = db.Column(db.Integer, ForeignKey("products.product_id"))