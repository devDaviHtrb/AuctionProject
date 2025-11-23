from myapp.setup.InitSqlAlchemy import db

class payment_statuses(db.Model):
    payment_status_id = db.Column(db.Integer, primary_key=True)
    payment_status = db.Column(db.String(255), nullable=False)
    payment_name = db.Column(db.String(255), nullable=False)
