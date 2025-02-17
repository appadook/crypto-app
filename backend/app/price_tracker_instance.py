from app.socketio_instance import socketio
from app.external.price_tracker import PriceTracker
import logging

logger = logging.getLogger(__name__)

try:
    price_tracker = PriceTracker(socketio)
    logger.info("PriceTracker initialized successfully with SocketIO instance")
except Exception as e:
    logger.error(f"Failed to initialize PriceTracker: {str(e)}")
    raise