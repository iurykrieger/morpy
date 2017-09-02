# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load env variables from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG = os.environ.get('DEBUG', True)
SECRET_KEY = os.environ.get('SECRET_KEY')
API_TOKEN = os.environ.get('API_TOKEN')
REDIS_URL = os.environ.get('REDIS_URL')

#Mongo envroinment configuration
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
