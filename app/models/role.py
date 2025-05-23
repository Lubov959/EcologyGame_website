from ..extensions import db


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    users = db.relationship('Users', back_populates='role', lazy=True)
    def __repr__(self):
        return f'<Roles {self.name}>'

