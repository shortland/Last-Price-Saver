import os

LOG_PATH = os.environ['INTERNAL_LOG_PATH']
LOG_LEVEL = os.environ['LOG_LEVEL']

QUOTE_SYMBOLS = (os.environ['QUOTE_SYMBOLS']).split(',')

API_KEY = os.environ['API_KEY']
REDIRECT_URI = os.environ['REDIRECT_URI']
TOKEN_PATH = os.environ['TOKEN_PATH']

MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')

PROMETHEUS_PORT = os.getenv('PROMETHEUS_PORT')
