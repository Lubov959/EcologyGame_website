import os
from app import create_app

from dotenv import load_dotenv
load_dotenv('.venv')

application = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Получаем порт из переменной окружения или используем 5000 по умолчанию
    application.run(host='0.0.0.0', port=port)  # Указываем хост и порт