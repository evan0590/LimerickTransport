# demo/settings.py
from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
NTA_API_KEY = environ.get('NTA_API_KEY')
