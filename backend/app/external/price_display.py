import logging
from datetime import datetime

class PriceDisplay:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.message_count = 0

    def display_prices(self, price_data):
        prices = price_data.get('prices', {})
        timestamp = price_data.get('last_update', datetime.now().isoformat())
        self.message_count += 1
        
        # Convert ISO timestamp to desired format
        dt = datetime.fromisoformat(timestamp)
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        
        output = [
            "\n=== LATEST CRYPTOCURRENCY PRICES ===",
            f"Last Update: {formatted_time}",
            f"Messages Received: {self.message_count}"
        ]
        
        for crypto in sorted(prices.keys()):
            output.append(f"\n{crypto}/USD prices:")
            output.append(f"Current state: {prices[crypto]}")
            for exchange, data in sorted(prices[crypto].items()):
                price = data['price']
                output.append(f"{exchange:<10} ${price:,.2f}")
        
        # Join all lines and log as a single message
        self.logger.info("\n".join(output))

        self.logger.info("\n\n\n")

# Global instance
price_display = PriceDisplay()