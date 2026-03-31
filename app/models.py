from app import db
from datetime import datetime

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created  = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    owner_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created     = db.Column(db.DateTime, default=datetime.utcnow)