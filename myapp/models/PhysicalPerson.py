from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class physical_persons(db.Model):
    user_id = db.Column(db.Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    rg =  db.Column(db.String(12), nullable=True) #False
    birth_date = db.Column(db.Date, nullable=True)
    gender =  db.Column(db.String(20), nullable=True)
