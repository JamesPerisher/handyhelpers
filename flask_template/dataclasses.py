from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = 'testing'
    id = db.Column(db.Integer, primary_key=True)

    string = db.Column(db.String(25))
    integer  = db.Column(db.Integer)
    date        = db.Column(db.DateTime, default=datetime.now)
