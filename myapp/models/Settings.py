from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class settings(db.Model):
    setting_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id", ondelete = "CASCADE"),  nullable = False)
    anonymous_mode = db.Column(db.Boolean, nullable = False, default = False)
    two_factor_auth = db.Column(db.Boolean, nullable = False, default = False)
