from myapp.setup.InitSqlAlchemy import db

class LegalEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CNPJ = db.Column(db.String(70), nullable= False)