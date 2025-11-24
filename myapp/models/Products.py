import secrets
from sqlalchemy import ForeignKey
from myapp.setup.InitSqlAlchemy import db

class products(db.Model):
    product_id =  db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_room = db.Column(db.String(64), unique=True, nullable=False, default=lambda:secrets.token_urlsafe(16))
    description =  db.Column(db.Text, nullable=True)
    min_bid = db.Column(db.DECIMAL(12, 2), nullable=False, default = float(0))
    start_datetime =  db.Column(db.DateTime(timezone=True), nullable=True)
    product_status = db.Column(db.Integer, ForeignKey("product_statuses.product_status_id"), default = 1) #sorry :/ ..........
    street_name = db.Column(db.String(255), nullable=True)
    street_number = db.Column(db.String(6), nullable=True)
    apt = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.CHAR(9), nullable=True)
    district = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.CHAR(2), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id", ondelete = "CASCADE"))
    #FK 
    category = db.Column(db.Integer, ForeignKey("categories.category_id"), default = 1)


    #changes
    end_datetime = db.Column(db.DateTime(timezone=True), nullable=True)
    duration = db.Column(db.Integer, nullable = False) # In Seconds
    first_value = db.Column(db.Integer, nullable = False, default = 0)

