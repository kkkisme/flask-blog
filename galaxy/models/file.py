from galaxy import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_name = db.Column(db.String(50))
    name = db.Column(db.String(50), unique=True, nullable=False)
    ext = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'File({self.id}, {self.name})'
