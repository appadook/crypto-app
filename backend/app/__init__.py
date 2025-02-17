# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from .socketio_instance import socketio
import logging
from app.config.settings import Config
from app.websocket import init_websocket
from app.routes.routes import main_bp  # Import the price routes blueprint
from app.routes.test_routes import test_bp  # Import test routes

def create_app(config_class=Config):
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS with specific origins
    CORS(app)

    # Initialize SocketIO with the app
    socketio.init_app(
        app,
        cors_allowed_origins="*",  # Allow all origins
        ping_interval=25,
        ping_timeout=120,
        async_mode='threading'
    )

    # Initialize WebSocket handlers
    init_websocket(socketio)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp)
    

    return app