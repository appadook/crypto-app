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
    
    def normalize_pair(self, pair: str) -> str:
        """
        Convert 'EURUSD' format to 'EUR' since we're always working relative to USD
        """
        if pair.endswith('USD'):
            return pair[:-3]  # Remove 'USD' suffix
        return pair
    
    def unpack_data(self, data):
        inc = data.split('|')
        out = {}
        for i, key in enumerate(self.order):
            out[key] = inc[i]
        out["name"] = self.mapping[out["name"]]
        out["time"] = float(out["time"]) / self.time_mult + self.start_time
        
        # Normalize the currency pair name and store latest data
        if 'name' in out and 'ask' in out:
            normalized_name = self.normalize_pair(out['name'])
            self.latest_data[normalized_name] = {
                'rate': float(out['ask']),
                'timestamp': out['time']
            }
            # Update the name in the output to match the normalized format
            out['name'] = normalized_name
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
                processed_data = self.unpack_data(msg)
                if processed_data and 'name' in processed_data and 'ask' in processed_data:
                    # Return data in the format expected by price_tracker
                    return {
                        'name': processed_data['name'],
                        'ask': float(processed_data['ask']),
                        'timestamp': processed_data['time']
                    }
                return processed_data
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
    
 