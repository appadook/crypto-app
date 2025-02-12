from app.socketio_instance import socketio
from app.external.price_tracker import PriceTracker

price_tracker = PriceTracker(socketio)