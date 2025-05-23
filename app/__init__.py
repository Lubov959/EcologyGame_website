from flask import Flask
from .extensions import migrate, db, login_manager, mail
from .config import Config
from .routes.user import user
from .routes.main import main
from .routes.role import role
from .models.user import Users
from .models.progress import Progress
from .models.role import Roles
from .models.type import Types
from .routes.Iquiz import Iquiz


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    # Импортируем пакет моделей целиком — импортируя модели из __init__.py, мы НЕ создаём циклы


    # Регистрируем blueprints
    app.register_blueprint(user)
    app.register_blueprint(role)
    app.register_blueprint(main)
    app.register_blueprint(Iquiz)

    # Инициализация Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'Для доступа необходима авторизация'

    with app.app_context():
        # Чтобы tables создавались однократно
        db.create_all()
    return app
