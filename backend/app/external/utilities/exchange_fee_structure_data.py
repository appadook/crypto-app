fee_structures = {
    "coinbase": {
        "trading_fee_buy": 0.0,  # 0% for Coinbase One
        "spread_fee_buy": 0.005,  # ~0.50% spread
        "payment_fee": 0.0,  # ACH is free
        "network_fee": 0.0,  # Waived for Coinbase One
        "blockchain_fee": 0.0,  # Covered by Coinbase One
        "trading_fee_sell": 0.0,  # 0% for Coinbase One
        "spread_fee_sell": 0.005,  # ~0.50% spread
        "withdrawal_fee": {
            "crypto": {
                "BTC": 0.0,  # Free for BTC (Coinbase One)
                "ETH": 0.0,  # Free for ETH (Coinbase One)
                # Add other cryptocurrencies and their fees here
            },
            "fiat": {
                "USD": {"ACH": 0.0, "Wire": 10.0},  # ACH is free, Wire is $10
                "EUR": {"SEPA": 0.15},  # 0.15 EUR for SEPA
                "GBP": {"Faster Payments": 0.0},  # Free for Faster Payments
            },
        },
    },
    "binance": {
        "trading_fee_buy": 0.00015,  # 0.015% taker fee for VIP 9
        "spread_fee_buy": 0.0005,  # Small spread (~0.05%)
        "payment_fee": 0.0,  # Most methods are free
        "network_fee": 0.0,  # Binance covers withdrawal fees for some currencies
        "blockchain_fee": "varies",  # Passed to the user, depends on network congestion
        "trading_fee_sell": 0.00015,  # 0.015% taker fee for VIP 9
        "spread_fee_sell": 0.0005,  # Small spread (~0.05%)
        "withdrawal_fee": {
            "crypto": {
                "BTC": 0.0005,  # 0.0005 BTC withdrawal fee
                "ETH": 0.01,  # 0.01 ETH withdrawal fee
                # Add other cryptocurrencies and their fees here
            },
            "fiat": {
                "USD": {"SWIFT": 15.0},  # $15–$30 for SWIFT
                "EUR": {"SEPA": 1.0},  # 1 EUR for SEPA
                "GBP": {"Faster Payments": 1.0},  # 1 GBP for Faster Payments
            },
        },
    },
}