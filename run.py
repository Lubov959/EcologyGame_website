import os
from app import create_app

from dotenv import load_dotenv
load_dotenv('.venv')

application = create_app()
