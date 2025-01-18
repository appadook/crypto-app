import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()
API_KEY = os.getenv('COINAPI_KEY')

# Create a nested dictionary for crypto prices
crypto_prices = {
    'BTC': {},  # Exchange -> price mapping for Bitcoin
    'ETH': {}   # Exchange -> price mapping for Ethereum
}

message_count = 0
COST_PER_MESSAGE = 0.0001
last_clear_time = datetime.now()

def format_price(message):
    global message_count, last_clear_time
    message_count += 1
    current_time = datetime.now()
    
    data = json.loads(message)
    symbol = data['symbol_id']
    price = data['price']
    exchange = symbol.split('_')[0]
    timestamp = data['time_exchange']
    
    # Process both USD and USDT pairs
    if not (symbol.endswith('_USD') or symbol.endswith('_USDT') or symbol.endswith('_EUR')):
        return
    
    # Clean up exchange name for Binance
    if 'BINANCE' in exchange:
        exchange = 'BINANCE'
    
    # Determine crypto type and update price
    if 'BTC' in symbol:
        crypto_prices['BTC'][exchange] = price
    elif 'ETH' in symbol:
        crypto_prices['ETH'][exchange] = price
    
    # Print debug message
    # print(f"\nDebug - Received message: {symbol} - ${price}")
    
    # Display all prices every 2 seconds
    if (current_time - last_clear_time).total_seconds() >= 2:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n=== Latest Cryptocurrency Prices ===")
        print(f"Last Update: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Messages Received: {message_count}")
        print(f"Estimated Cost: ${message_count * COST_PER_MESSAGE:.4f}")
        print(f"Remaining Credit: ${max(25 - message_count * COST_PER_MESSAGE, 0):.4f}\n")
        
        # Print current state of all prices
        for crypto in crypto_prices:
            print(f"\n{crypto}/USD prices:")
            print(f"Current state: {crypto_prices[crypto]}")
            for exchange, price in sorted(crypto_prices[crypto].items()):
                print(f"{exchange:<10} ${price:,.2f}")

        last_clear_time = current_time

async def connect_to_coinapi():
    uri = "wss://ws.coinapi.io/v1/"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket connection established...")
            
            # Updated authentication message with correct Binance symbols
            auth_message = {
                "type": "hello",
                "apikey": API_KEY,
                "heartbeat": False,
                "subscribe_data_type": ["trade"],
                "subscribe_filter_symbol_id": [
                    # "BITSTAMP_SPOT_BTC_USD", "BITSTAMP_SPOT_ETH_USD",
                    # "KRAKEN_SPOT_BTC_USD", "KRAKEN_SPOT_ETH_USD",
                    # "BINANCE_SPOT_BTC_USDT", "BINANCE_SPOT_ETH_USDT",  # Changed from BINANCE to BINANCEUS
                    # "COINBASE_SPOT_BTC_USD", "COINBASE_SPOT_ETH_USD"
                    # "COINBASE_SPOT_BTC_EUR", "BITSTAMP_SPOT_BTC_EUR",
                    # "KRAKEN_SPOT_BTC_EUR",
                ]
            }
            
            print("Sending authentication message...")
            await websocket.send(json.dumps(auth_message))
            print("Authentication message sent, waiting for response...")
            
            while True:
                try:
                    message = await websocket.recv()
                    # print(f"Message received: {message}")
                    
                    # Parse the message
                    data = json.loads(message)
                    
                    # Handle authentication response
                    if data.get('type') == 'error':
                        print(f"Authentication error: {data}")
                        return
                    
                    # If we get here, process the trade data
                    if 'price' in data:
                        format_price(message)
                    
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed unexpectedly")
                    break
                except json.JSONDecodeError:
                    print(f"Failed to decode message: {message}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break
    
    except Exception as e:
        print(f"Failed to establish WebSocket connection: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(connect_to_coinapi())
    except KeyboardInterrupt:
        print("\nExiting...")
        print(f"Total messages received: {message_count}")
        print(f"Total estimated cost: ${message_count * COST_PER_MESSAGE:.4f}")




## MESSAGE RECEIVED
# {"time_exchange":"2025-01-14T16:49:58.3318050Z","time_coinapi":"2025-01-14T16:49:58.3368845Z","uuid":"fa42708a-ca7b-4d48-9bf8-68d23b416751","price":95495.96,"size":0.00310908,"taker_side":"BUY","symbol_id":"COINBASE_SPOT_BTC_USD","sequence":5231604,"type":"trade"}