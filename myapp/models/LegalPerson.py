from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class legal_persons(db.Model):
    user_id = db.Column(db.Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    cnpj = db.Column(db.String(70), nullable= False)
    state_tax_registration = db.Column(db.CHAR(17), nullable=True)
    legal_business_name =  db.Column(db.String(255), nullable=False)
    trade_name = db.Column(db.String(255), nullable=False)
    scrap_purchase_authorization =  db.Column(db.Boolean,  default=False, nullable=True)



