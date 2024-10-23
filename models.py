from datetime import datetime
from app import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_to = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(128))
