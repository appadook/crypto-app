from flask import Flask
from flask_socketio import SocketIO
import logging
from app.config.settings import Config
from app.websocket import init_websocket

socketio = SocketIO()

def create_app(config_class=Config):
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     ping_interval=config_class.WEBSOCKET_PING_INTERVAL,
                     ping_timeout=config_class.WEBSOCKET_PING_TIMEOUT,
                     async_mode='threading')  # Add this line

    init_websocket(socketio)

    return app