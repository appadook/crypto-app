# backend/run.py
from app import create_app
from app.socketio_instance import socketio  # Updated import
from app.external.websocket_client import start_external_websockets, stop_external_websockets  # Ensure this line is correct
from app.external.strategies.coinapi_strategy import CoinAPIStrategy
from app.external.strategies.exchange_api_strategy import ExchangeAPIStrategy
from app.price_tracker_instance import price_tracker 

app = create_app()
socketio.init_app(app)  

# coinapi_strategy = CoinAPIStrategy(price_tracker)  # Instantiate the strategy with the price tracker
# xchangeapi_strategy = ExchangeAPIStrategy(price_tracker)  # Instantiate the strategy with the price tracker

def broadcast_update(event, data):
    socketio.emit(event, data)

# Add connect event handler for testing
@socketio.on("connect")
def test_connect():
    print("Client connected")
    socketio.emit("client data", {"message": "Hello from backend"})


if __name__ == '__main__':
    try:
        # Start external WebSocket client in a separate thread
        start_external_websockets(broadcast_update)
        # Run Flask-SocketIO app
        socketio.run(app, 
                    host='0.0.0.0',
                    port=5000,
                    debug=True,
                    use_reloader=False)  # Disable reloader to prevent duplicate WebSocket connections
    except KeyboardInterrupt:
        stop_external_websockets()