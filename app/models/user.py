from ..extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(300), nullable=False, unique=True)
    user_name = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    theme = db.Column(db.String(10), default='light')


    role = db.relationship('Roles', back_populates='users', lazy=True)
    progress = db.relationship('Progress', back_populates='user', lazy=True) # Используем строковую ссылку
    def __repr__(self):
        return f'<User  {self.user_name}, Role: {self.role.name}>'
    def has_role(self, role_name):
        return self.role.name == role_name
    def get_id(self):
        return str(self.id)