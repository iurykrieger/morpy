# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load env variables from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG = os.environ.get('DEBUG')
SECRET_KEY = os.environ.get('SECRET_KEY')
API_TOKEN = os.environ.get('API_TOKEN')
REDIS_URL = os.environ.get('REDIS_URL')
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
MONGO_URI = os.environ.get('MONGO_URI')
