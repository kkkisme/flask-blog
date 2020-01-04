from galaxy import db
from datetime import datetime


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_name = db.Column(db.String(50))
    name = db.Column(db.String(50), unique=True, nullable=False)
    ext = db.Column(db.String(10), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    create_by = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'File({self.id}, {self.name})'
