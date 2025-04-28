# import boto3
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager


# login_manager = LoginManager()
# bcrypt=Bcrypt()
#
# # Инициализация базы данных и миграций
# db = SQLAlchemy()
migrate = Migrate()
#
# bucket_name = None
# file_path = None
# s3 = None  # Изначально s3 будет None
#
#
# def init_s3(app):
#     global s3, bucket_name, file_path
#     bucket_name = app.config['S3_BUCKET_NAME']
#     file_path = app.config['S3_ENDPOINT_URL']
#
#     if not bucket_name or not file_path:
#         print("Error: S3_BUCKET_NAME or S3_ENDPOINT_URL not set in configuration.")
#         return
#
#     try:
#         session = boto3.session.Session()
#         s3 = session.client(
#             service_name='s3',
#             endpoint_url=app.config['S3_ENDPOINT_URL'],
#             aws_access_key_id=app.config['S3_ACCESS_KEY_ID'],
#             aws_secret_access_key=app.config['S3_SECRET_ACCESS_KEY']
#         )
#
#         if not s3:
#             print("S3 client could not be created. Exiting upload.")
#             return None
#         print("S3 client initialized successfully")
#     except Exception as e:
#         print(f"S3 client could not be created: {str(e)}")
#         return
