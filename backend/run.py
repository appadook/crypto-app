# backend/run.py
from gevent import monkey
monkey.patch_all()  # This needs to be at the very top!
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
from datetime import datetime
from app.external.websocket_client import start_external_websockets, stop_external_websockets

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Socket.IO with the app
from app.socketio_instance import socketio
socketio.init_app(app)

# Initialize PriceTracker after socketio is fully set up
from app.price_tracker_instance import price_tracker

@app.route('/')
def index():
    return 'Crypto App WebSocket Server Running'

def broadcast_update(event, data):
    try:
        socketio.emit(event, data)
        logger.debug(f"Broadcasted event {event} with data: {data}")
    except Exception as e:
        logger.error(f"Error broadcasting event {event}: {str(e)}")

@socketio.on("connect")
def handle_connect():
    try:
        client_id = request.sid
        transport = request.environ.get('wsgi.url_scheme', 'unknown')
        headers = dict(request.headers)
        logger.info(f"Client attempting to connect - ID: {client_id}")
        logger.info(f"Connection details - Transport: {transport}")
        logger.info(f"Headers: {headers}")
        
        socketio.emit("connection_status", {
            "status": "connected",
            "id": client_id,
            "server_time": datetime.now().isoformat(),
            "transport": transport
        })
        logger.info(f"Client successfully connected - ID: {client_id}")
        
        # Send a hello message when client connects
        price_tracker.emit_hello_message()
    except Exception as e:
        logger.error(f"Error handling connection: {str(e)}", exc_info=True)

@socketio.on("disconnect")
def handle_disconnect():
    try:
        client_id = request.sid
        logger.info(f"Client disconnected - ID: {client_id}")
    except Exception as e:
        logger.error(f"Error handling disconnect: {str(e)}")

if __name__ == '__main__':
    try:
        logger.info("="*50)
        logger.info("Starting the application...")
        port = 5001
        logger.info(f"Starting Flask-SocketIO server on http://localhost:{port}")
        logger.info("CORS enabled for all origins (*)")
        logger.info("WebSocket and polling transports enabled")
        
        # Start external WebSocket connections
        logger.info("Starting external WebSocket connections...")
        start_external_websockets(broadcast_update)
        
        socketio.run(
            app,
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
        stop_external_websockets()
    except Exception as e:
        logger.error("="*50)
        logger.error("Failed to start server:")
        logger.error(str(e))
        stop_external_websockets()  # Ensure we stop websockets even on error
        raise