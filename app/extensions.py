# import boto3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


login_manager = LoginManager()
bcrypt=Bcrypt()

# Инициализация базы данных и миграций
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
