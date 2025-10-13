from __future__ import annotations
from flask_login import UserMixin
from typing import Tuple, Optional
from myapp.setup.InitSqlAlchemy import db

class users(db.Model, UserMixin):
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable= False)
    username = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String(400), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cpf =  db.Column(db.CHAR(11), nullable=True) #False
    photo = db.Column(db.String(255), nullable=True)
    cellphone1 = db.Column(db.CHAR(14), nullable=True) #False
    cellphone2 = db.Column(db.CHAR(14), nullable=True)
    landline = db.Column(db.CHAR(13), nullable=True)
    wallet = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)
    admin_user = db.Column(db.Boolean, nullable=False)
    active_auction_number = db.Column(db.SmallInteger, nullable=False)
    password_token_expiration_datetime = db.Column(db.DateTime, nullable=True)
    api_token = db.Column(db.String(255), nullable=True)
    password_token = db.Column(db.String(255), nullable=True)

    authenticated = True
    active = True
    anonymous = False

    def get_id(self):
        return str(self.user_id)
    
    @classmethod
    def get_by_email(cls, wanted_email:str) -> Optional[users]:
        return db.session.query(cls).filter(
            cls.email == wanted_email
        ).first()
    
    def delete(self) -> Tuple[bool, str]:
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "ok"
        except Exception as e:
            db.session.rollback()
            return False, e

