from enum import Enum


class CollectorType(Enum):
    FUNDING_RATE = "funding_rate"
    LONG_SHORT_RATIO = "long_short_ratio"
    OHLCV = "ohlcv"
    OPEN_INTEREST = "open_interest"
    ORDERBOOK = "orderbook"
    TAKER_BUY_SELL = "taker_buy_sell"
