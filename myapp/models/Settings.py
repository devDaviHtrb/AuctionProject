from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class settings(db.Model):
    setting_id = db.Column(db.Integer, primary_key=True)
    anonymous_mode =  user_id = db.Column(db.Integer, nullable= False)
    two_factor_auth = user_id = db.Column(db.Integer, nullable= False)
    user_id =  user_id = db.Column(db.Integer, ForeignKey("users.user_id"))