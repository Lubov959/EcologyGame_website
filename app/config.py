import os

class Config(object):
    APPNAME = 'app'
    ROOT= os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/uploads'
    SERVER_PATH= ROOT+UPLOAD_PATH

    # USER = os.environ.get('POSTGRES_USER', 'adm')
    # PASSWORD =os.environ.get('POSTGRES_PASSWORD', 'adm')
    # HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    # PORT = os.environ.get('POSTGRES_PORT', 5431)
    # DB = os.environ.get('POSTGRES_DB', 'db_tv')
    #
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SECRET_KEY ='duuwkj983g97q02jkd7302jdfujf73d'
    #

# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Или используйте in-memory: 'sqlite:///:memory:'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     TESTING = True
#     DEBUG = True

