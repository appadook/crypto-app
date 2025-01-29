import logging
from datetime import datetime
class PriceDisplay:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.message_count = 0

    def _format_timestamp(self, timestamp) -> str:
        """Format timestamp with error handling"""
        try:
            if not isinstance(timestamp, str):
                timestamp = str(timestamp)
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            self.logger.error(f"Error formatting timestamp: {e}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _format_crypto_prices(self, prices: dict) -> list:
        """Helper method to format cryptocurrency prices"""
        output = []
        for crypto in sorted(prices.keys()):
            output.append(f"\n{crypto} prices:")
            for exchange in sorted(prices[crypto].keys()):
                output.append(f"\n  {exchange}:")
                for fiat, data in sorted(prices[crypto][exchange].items()):
                    price = data['price']
                    fiat_time = datetime.fromisoformat(data['timestamp']).strftime('%H:%M:%S')
                    output.append(f"    {fiat}: {price:.2f} ({fiat_time})")
        return output

    def _format_exchange_rates(self, exchange_rates: dict) -> list:
        """Helper method to format exchange rates"""
        output = []
        try:
            if exchange_rates:
                output.append("\n=== EXCHANGE RATES ===")
                for pair, rate_data in sorted(exchange_rates.items()):
                    if rate_data and isinstance(rate_data, dict):
                        rate = rate_data.get('rate')
                        try:
                            timestamp = str(rate_data.get('timestamp')) if rate_data.get('timestamp') else datetime.now().isoformat()
                            rate_time = datetime.fromisoformat(timestamp).strftime('%H:%M:%S')
                            output.append(f"{pair}: {rate:.4f} ({rate_time})")
                        except Exception as e:
                            self.logger.error(f"Timestamp error for {pair}: {e}")
                            output.append(f"{pair}: {rate:.4f}")
                    elif isinstance(rate_data, (int, float)):
                        output.append(f"{pair}: {rate_data:.4f}")
        except Exception as e:
            self.logger.error(f"Error formatting exchange rates: {e}")
        return output

    def display_prices(self, price_data):
        prices = price_data.get('prices', {})
        exchange_rates = price_data.get('exchange_rates', {})
        timestamp = price_data.get('last_update')
        self.message_count += 1
        
        formatted_time = self._format_timestamp(timestamp)
        
        output = [
            "\n=== LATEST CRYPTOCURRENCY PRICES ===",
            f"Last Update: {formatted_time}",
            f"Messages Received: {self.message_count}"
        ]
        
        output.extend(self._format_crypto_prices(prices))
        output.extend(self._format_exchange_rates(exchange_rates))
        
        print('\n'.join(output))
        print("\n" + "="*40)

    def display_arbitrage(self, price_data):
        prices = price_data.get('prices', {})
        exchange_rates = price_data.get('exchange_rates', {})
        eur_usd_rate = exchange_rates.get('EURUSD', {}).get('rate')

        if not eur_usd_rate:
            self.logger.error("EURUSD exchange rate not available.")
            return

        output = ["\n=== FIAT PRICE COMPARISON (EUR to USD) ==="]
        
        for crypto, exchanges in prices.items():
            for exchange, fiats in exchanges.items():
                if 'EUR' in fiats and 'USD' in fiats:
                    eur_price = fiats['EUR']['price']
                    usd_price = fiats['USD']['price']
                    converted_eur_price = eur_price * eur_usd_rate
                    output.append(f"\n{crypto} on {exchange}:")
                    output.append(f"  EUR: {eur_price:.2f} (Converted to USD: {converted_eur_price:.2f})")
                    output.append(f"  USD: {usd_price:.2f}")
                    if converted_eur_price != usd_price:
                        price_diff = abs(converted_eur_price - usd_price)
                        arbitrage_action = "BUY EUR" if converted_eur_price < usd_price else "BUY USD"
                        output.append(f"  ARBITRAGE: Price difference is {price_diff:.2f} USD ({arbitrage_action})")
        
        print('\n'.join(output))
        print("\n" + "="*40)

# Global instance
price_display = PriceDisplay()