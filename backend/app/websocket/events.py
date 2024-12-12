from flask_socketio import emit
from . import ws_manager
import logging

logger = logging.getLogger(__name__)

def init_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        try:
            ws_manager.handle_connect()
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    @socketio.on('disconnect')
    def handle_disconnect():
        ws_manager.handle_disconnect()

    @socketio.on('subscribe')
    def handle_subscribe(data):
        # Add subscription logic here
        emit('subscribed', {'status': 'success'})

    @socketio.on('subscribe_external')
    def handle_external_subscribe(data):
        try:
            sources = data.get('sources', [])
            valid_sources = {'coinapi', 'xchange'}
            
            if not sources or not all(s in valid_sources for s in sources):
                emit('error', {'message': 'Invalid sources specified'})
                return

            if ws_manager.add_subscription(request.sid, sources):
                emit('external_subscribed', {
                    'status': 'success',
                    'sources': sources
                })
            else:
                emit('error', {'message': 'Subscription failed'})
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            emit('error', {'message': 'Internal server error'})

    @socketio.on('get_latest_prices')
    def handle_get_prices():
        try:
            from app.external.websocket_client import price_tracker
            prices = price_tracker.get_latest_prices()
            emit('price_update', {
                'all_prices': prices,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error getting prices: {str(e)}")
            emit('error', {'message': 'Failed to get latest prices'})

    @socketio.on('subscribe_feed')
    def handle_feed_subscribe(data):
        try:
            feed_type = data.get('feed')
            if feed_type in ['price', 'volume', 'orderbook']:
                if ws_manager.add_subscription(request.sid, [feed_type]):
                    emit('feed_subscribed', {
                        'status': 'success',
                        'feed': feed_type
                    })
                else:
                    emit('error', {'message': 'Subscription failed'})
            else:
                emit('error', {'message': 'Invalid feed type'})
        except Exception as e:
            logger.error(f"Feed subscription error: {str(e)}")
            emit('error', {'message': 'Internal server error'})