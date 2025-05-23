import os

class Config(object):
    APPNAME = 'app'
    ROOT= os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/uploads'
    SERVER_PATH= ROOT+UPLOAD_PATH
    IQUIZ_PATH = os.path.join(ROOT, 'static', 'Iquiz')

    @classmethod
    def get_json_path(cls, game_name):
        return os.path.join(cls.IQUIZ_PATH, f'{game_name}.json')

    USER = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWORD =os.environ.get('POSTGRES_PASSWORD', 'lubov')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5432)
    DB = os.environ.get('POSTGRES_DB', 'db_eco')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY ='duuwkj983g97q02jkd7302jdfinnv947'


    # SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = True

    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'lv_7705@mail.ru'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
