from typing import Dict, TypedDict

class PriceData(TypedDict):
    price: float
    timestamp: str

class ExchangeData(TypedDict):
    USD: PriceData
    EUR: PriceData

class CryptoData(TypedDict):
    COINBASE: ExchangeData
    BINANCE: ExchangeData

PriceDataType = Dict[str, Dict[str, Dict[str, PriceData]]]