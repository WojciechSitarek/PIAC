from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class GuestBookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GuestBookEntry {self.nick}>'
