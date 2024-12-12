
from .manager import WebSocketManager

ws_manager = None

def init_websocket(socketio):
    global ws_manager
    ws_manager = WebSocketManager(socketio)
    
    from . import events
    events.init_events(socketio)