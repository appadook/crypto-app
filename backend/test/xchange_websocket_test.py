import asyncio
import websockets
import json
import ssl
from dotenv import load_dotenv
import os
from datetime import datetime

class XChangeProcessor:
    def __init__(self):
        self.start_time = None
        self.mapping = None
        self.order = None
        self.time_mult = None
        
    def unpack_init(self, data):
        meta = json.loads(data)
        self.start_time = meta['start_time']
        self.mapping = meta['mapping']
        self.order = meta['order']
        self.time_mult = meta['time_mult']
        return meta
    
    def unpack_err_pair(self, data):
        return json.loads(data)
    
    def unpack_data(self, data):
        inc = data.split('|')
        out = {}
        for i, key in enumerate(self.order):
            out[key] = inc[i]
        out["name"] = self.mapping[out["name"]]
        out["time"] = float(out["time"]) / self.time_mult + self.start_time
        return out
    
    def process_message(self, data):
        t = data[0]
        msg = data[1:]
        
        try:
            if t == '0':
                return self.unpack_init(msg)
            elif t in ['7', '8', '9']:
                return self.unpack_err_pair(msg)
            elif t == '1':
                return self.unpack_data(msg)
            elif t == '2':
                return "heartbeat"
            else:
                return None
        except Exception as e:
            print(f"Error processing message: {e}")
            return None

async def connect_to_xchangeapi():
    uri = f"wss://api.xchangeapi.com/websocket/live?api-key={XCHANGE_API_KEY}"
    pairs = ["EURUSD", "GBPCHF"]
    processor = XChangeProcessor()
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            print("Connection established!")
            
            # Send subscription
            await websocket.send(json.dumps({"pairs": pairs}))
            print("Subscription sent")
            
            while True:
                message = await websocket.recv()
                result = processor.process_message(message)
                if result:
                    print(json.dumps(result, indent=2))
                
    except Exception as e:
        print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    XCHANGE_API_KEY = os.getenv('XCHANGEAPI_KEY')
    if not XCHANGE_API_KEY:
        raise ValueError("XCHANGEAPI_KEY not found in environment variables")
        
    try:
        asyncio.run(connect_to_xchangeapi())
    except KeyboardInterrupt:
        print("\nExiting...")