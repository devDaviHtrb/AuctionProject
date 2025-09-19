from flask_login import UserMixin
from myapp.setup.InitSqlAlchemy import db

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable= False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(1000), nullable=False)

    authenticated = True
    active = True
    anonymous = False

