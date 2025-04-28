from flask import Flask
from .extensions import migrate
from .config import Config
from .routes.main import main

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.register_blueprint(main)

    # db.init_app(app)
    # migrate.init_app(app, db)


    # login_manager.init_app(app)
    # login_manager.login_view = 'user.login'
    # login_manager.login_message_category = 'Для доступа необходима авторизаиця'


    # with app.app_context():
    #     db.create_all()

    return app


    # app = create_app()
    # app.run(debug=True, host='0.0.0.0', port=5000)
