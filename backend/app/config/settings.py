
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    COINAPI_KEY = os.environ.get('COINAPI_KEY')
    XCHANGEAPI_KEY = os.environ.get('XCHANGEAPI_KEY')
    WEBSOCKET_PING_INTERVAL = 25
    WEBSOCKET_PING_TIMEOUT = 120