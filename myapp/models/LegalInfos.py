from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class legal_infos(db.Model):
    legal_infos_id = db.Column(db.Integer, primary_key=True)
    process_number = db.Column(db.CHAR(25), nullable=False)
    court =db.Column(db.String(255), nullable=False)
    case_type =   db.Column(db.Integer, ForeignKey("case_types.case_type_id", ondelete = "CASCADE"))
    plaintiff =db.Column(db.String(255), nullable=False)
    defendant =db.Column(db.String(255), nullable=False)
    judge_name =db.Column(db.String(255), nullable=False)
    extra_notes =  db.Column(db.Text, nullable=True)
    product_id = db.Column(db.Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    