# backend/app/__init__.py
from flask import Flask
from .socketio_instance import socketio
from flask_socketio import SocketIO
import logging
from app.config.settings import Config
from app.websocket import init_websocket
from app.routes.routes import main_bp  # Import the price routes blueprint
from app.external.strategies.coinapi_strategy import CoinAPIStrategy

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

    # Register the blueprint for price routes
    app.register_blueprint(main_bp)

    return app