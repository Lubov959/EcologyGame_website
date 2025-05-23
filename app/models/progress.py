from ..extensions import db

class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_name = db.Column(db.String(300), nullable=False)
    progress_scene = db.Column(db.Integer)
    progress_ball = db.Column(db.Integer)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Используем строковые ссылки на классы
    type = db.relationship('Types', back_populates='progress', lazy=True)
    user = db.relationship('Users', back_populates='progress', lazy=True)
    def has_type(self, type_name):
        return self.type.name == type_name
    def get_id(self):
        return str(self.id)