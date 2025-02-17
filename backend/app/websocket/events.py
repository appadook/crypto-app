from flask_socketio import emit
from flask import request
from . import ws_manager
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def init_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        """Handle new client connection"""
        try:
            if ws_manager.handle_connect():
                emit('connection_status', {'status': 'connected', 'client_id': request.sid})
            else:
                return False
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        ws_manager.handle_disconnect()

    @socketio.on('subscribe_exchange')
    def handle_exchange_subscribe(data):
        """Handle subscription to exchange data"""
        try:
            sources = data.get('sources', [])
            valid_sources = {'coinapi', 'xchange'}
            
            if not sources or not all(s in valid_sources for s in sources):
                emit('error', {'message': 'Invalid exchange sources specified'})
                return

            if ws_manager.add_subscription(request.sid, sources):
                emit('exchange_subscribed', {
                    'status': 'success',
                    'sources': sources
                })
            else:
                emit('error', {'message': 'Exchange subscription failed'})
        except Exception as e:
            logger.error(f"Exchange subscription error: {str(e)}")
            emit('error', {'message': 'Internal server error'})

    @socketio.on('subscribe_feed')
    def handle_feed_subscribe(data):
        """Handle subscription to specific data feeds"""
        try:
            feeds = data.get('feeds', [])
            valid_feeds = {'price', 'volume', 'orderbook', 'trades'}
            
            if not feeds or not all(f in valid_feeds for f in feeds):
                emit('error', {'message': 'Invalid feed types specified'})
                return

            if ws_manager.add_feed(request.sid, feeds):
                emit('feed_subscribed', {
                    'status': 'success',
                    'feeds': feeds
                })
            else:
                emit('error', {'message': 'Feed subscription failed'})
        except Exception as e:
            logger.error(f"Feed subscription error: {str(e)}")
            emit('error', {'message': 'Internal server error'})

    @socketio.on('get_latest_prices')
    def handle_get_prices():
        """Handle request for latest price data"""
        try:
            from app.price_tracker_instance import price_tracker
            prices = price_tracker.get_latest_prices()
            emit('price_update', {
                'all_prices': prices,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error getting prices: {str(e)}")
            emit('error', {'message': 'Failed to get latest prices'})

    @socketio.on('get_client_status')
    def handle_client_status():
        """Handle request for client connection status"""
        try:
            client_info = ws_manager.get_client_info(request.sid)
            if client_info:
                emit('client_status', {
                    'status': 'active',
                    'subscriptions': list(client_info['subscriptions']),
                    'feeds': list(client_info['feeds']),
                    'connected_at': client_info['connected_at']
                })
            else:
                emit('error', {'message': 'Client not found'})
        except Exception as e:
            logger.error(f"Error getting client status: {str(e)}")
            emit('error', {'message': 'Failed to get client status'})