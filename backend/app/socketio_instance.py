from flask_socketio import SocketIO
import logging

logger = logging.getLogger(__name__)

# Create a single SocketIO instance
socketio = SocketIO(
    cors_allowed_origins="*",  # Allow all origins
    async_mode='gevent',  # Use gevent as async mode
    logger=True,
    engineio_logger=True,
    ping_timeout=120,
    ping_interval=25,
    transports=['polling', 'websocket']  # Allow polling fallback
)

# Export the instance
__all__ = ['socketio']
