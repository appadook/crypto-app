FASTER_PAYMENTS = "Faster Payments"

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
                "GBP": {FASTER_PAYMENTS: 0.0},  # Free for Faster Payments
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
                "GBP": {FASTER_PAYMENTS: 1.0},  # 1 GBP for Faster Payments
            },
        },
    },
    "bitstamp": {  
        "trading_fee_buy": 0.0003,  # 0.03% taker fee (VIP tier: $20M+ 30-day volume)  
        "spread_fee_buy": 0.0,  # No explicit spread fee (dynamic market spread)  
        "payment_fee": {  
            "ACH": 0.0,  # Free ACH deposits  
            "Wire": 0.0,  # Free USD wire deposits  
            "Credit/Debit Card": 0.05,  # 5% card fee (unchanged for all tiers)  
        },  
        "network_fee": 0.0,  # Covered in withdrawal fees  
        "blockchain_fee": 0.0,  # Covered in withdrawal fees  
        "trading_fee_sell": 0.0003,  # 0.03% taker fee (VIP tier)  
        "spread_fee_sell": 0.0,  
        "withdrawal_fee": {  
            "crypto": {  
                "BTC": 0.0005,  # Fixed BTC withdrawal fee (unchanged by tier)  
                "ETH": 0.005,  # Fixed ETH withdrawal fee  
            },  
            "fiat": {  
                "USD": {"Wire": 0.001},  # 0.1% (min $7.5) for USD wire  
                "EUR": {"SEPA": 3.0},  # 3.00 EUR for SEPA  
                "GBP": {FASTER_PAYMENTS: 2.0},  # £2 fixed (assumed unchanged)  
            },  
        },  
    },  
    "kraken": {  
        "trading_fee_buy": 0.0016,  # 0.16% taker fee (highest volume tier: $10M+ 30-day trade volume)  
        "spread_fee_buy": 0.0,  # No explicit spread fee  
        "payment_fee": {  
            "ACH": 0.0,  # Free ACH deposits  
            "Wire": 0.0,  # Free domestic wire deposits  
        },  
        "network_fee": 0.0,  # Covered in withdrawal fees  
        "blockchain_fee": 0.0,  
        "trading_fee_sell": 0.0016,  # 0.16% taker fee  
        "spread_fee_sell": 0.0,  
        "withdrawal_fee": {  
            "crypto": {  
                "BTC": 0.00015,  # Fixed BTC withdrawal fee  
                "ETH": 0.0015,  # Fixed ETH withdrawal fee  
            },  
            "fiat": {  
                "USD": {"Wire": 5.0},  # $5 USD wire withdrawal  
                "EUR": {"SEPA": 1.0},  # 1.00 EUR SEPA  
                "GBP": {FASTER_PAYMENTS: 0.0},  # Free for GBP (confirmed)  
            },  
        },  
    },
}



    
