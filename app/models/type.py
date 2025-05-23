from ..extensions import db

class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)

    progress = db.relationship('Progress', back_populates='type', lazy=True)
    def __repr__(self):
        return f'<Types {self.name}>'