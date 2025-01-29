'''
This module calculates the fees for buying and selling cryptocurrencies on different exchanges.
Fees included are trading fees, spread fees, payment fees, network fees, blockchain fees, and withdrawal fees.
It allows us to calculate the total fees for a given transaction along with the price arbitrage between the biggest spread.
'''
from exchange_fee_structure_data import fee_structures

class FeeCalculator:
    """Calculator for cryptocurrency exchange fees"""
    FEE_STRUCTURES = fee_structures

    def __init__(self, exchange_buy, exchange_sell, crypto, crypto_amount, crypto_price_buy, crypto_price_sell, currency, withdrawal_method):
        self.exchange_buy = exchange_buy
        self.exchange_sell = exchange_sell
        self.crypto = crypto
        self.crypto_amount = crypto_amount
        self.crypto_price_buy = crypto_price_buy
        self.crypto_price_sell = crypto_price_sell
        self.currency = currency
        self.withdrawal_method = withdrawal_method

    def get_trading_fees(self, exchange, operation):
        """Get trading fees for an exchange"""
        return self.FEE_STRUCTURES[exchange][f"trading_fee_{operation}"]

    def get_spread_fees(self, exchange, operation):
        """Get spread fees for an exchange"""
        return self.FEE_STRUCTURES[exchange][f"spread_fee_{operation}"]

    def get_withdrawal_fee(self, exchange, currency, withdrawal_type, method=None, exchange_rate=1.0):
        """Get withdrawal fee based on currency type"""
        fees = self.FEE_STRUCTURES[exchange]["withdrawal_fee"]
        if withdrawal_type == "crypto":
            return fees["crypto"].get(currency, 0.0)
        fiat_fee = fees["fiat"][currency][method]
        # Normalize the fiat fee to USD using the exchange rate
        return fiat_fee * exchange_rate

    def calculate_fees(self):
        """Calculate total fees for buying and selling crypto"""
        
        # Calculate buying fees
        trading_fee_buy = self.crypto_amount * self.crypto_price_buy * self.get_trading_fees(self.exchange_buy, "buy")
        # spread_fee_buy = self.crypto_amount * self.crypto_price_buy * self.get_spread_fees(self.exchange_buy, "buy")
        payment_fee = self.crypto_amount * self.crypto_price_buy * self.FEE_STRUCTURES[self.exchange_buy]["payment_fee"]

        # Calculate selling fees
        trading_fee_sell = self.crypto_amount * self.crypto_price_sell * self.get_trading_fees(self.exchange_sell, "sell")
        # spread_fee_sell = self.crypto_amount * self.crypto_price_sell * self.get_spread_fees(self.exchange_sell, "sell")

        # Calculate withdrawal fee
        withdrawal_type = "crypto" if self.currency.upper() == self.crypto.upper() else "fiat"
        withdrawal_fee = self.get_withdrawal_fee(self.exchange_sell, self.currency, withdrawal_type, self.withdrawal_method, 1.0429)

        total_fees = (
            trading_fee_buy +
            # spread_fee_buy +
            payment_fee +
            trading_fee_sell +
            # spread_fee_sell +
            withdrawal_fee
        )

        return {
            "trading_fee_buy": trading_fee_buy,
            # "spread_fee_buy": spread_fee_buy,
            "payment_fee": payment_fee,
            "trading_fee_sell": trading_fee_sell,
            # "spread_fee_sell": spread_fee_sell,
            "withdrawal_fee": withdrawal_fee,
            "total_fees": total_fees,
            "price arbitrage": self.crypto_price_sell - self.crypto_price_buy,
        }
    
    def display_fees(self):
        """Calculate and display the total accumulated fees"""
        fees = self.calculate_fees()
        print("Fee Breakdown:")
        for key, value in fees.items():
            print(f"{key}: ${value:.2f}")


if __name__ == "__main__":
    # Example usage
    fee_calculator = FeeCalculator(
        exchange_buy="coinbase",
        exchange_sell="binance",
        crypto="BTC",
        crypto_amount=1,
        crypto_price_buy=102124.60,
        crypto_price_sell=102189.78,
        currency="USD",
        withdrawal_method="SWIFT"
    )

    fee_calculator.display_fees()

__all__ = ['FeeCalculator']
