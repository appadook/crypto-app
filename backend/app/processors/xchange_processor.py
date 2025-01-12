from .base_processor import DataProcessor  # Import the DataProcessor base class
import json

class XChangeProcessor(DataProcessor):
    def __init__(self):
        self.start_time = None
        self.mapping = None
        self.order = None
        self.time_mult = None
        self.latest_data = {}
        
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
        out["name"] = self.normalize_pair(self.mapping[out["name"]])  # Add normalization
        out["time"] = float(out["time"]) / self.time_mult + self.start_time
        
        # Store latest data
        if 'name' in out and 'ask' in out:
            self.latest_data[out['name']] = {
                'rate': float(out['ask']),
                'timestamp': out['time']
            }
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
        
    
    def get_latest_data(self) -> dict:
        """Implement abstract method from DataProcessor"""
        return self.latest_data
    
    def normalize_pair(self, pair: str) -> str:
        """Convert EURUSD format to EUR/USD format"""
        if len(pair) == 6:  # EURUSD format
            return f"{pair[:3]}/{pair[3:]}"
        return pair