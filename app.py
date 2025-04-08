from dataclasses import asdict, dataclass
import datetime
import os
from dotenv import load_dotenv
from influxdb_client_3 import InfluxDBClient3, Point
from alpaca.data.live import CryptoDataStream

load_dotenv()

alpaca_key = os.getenv("ALPACA_KEY")
alpaca_secret = os.getenv("ALPACA_SECRET")
influx_token = os.getenv("INFLUXDB_TOKEN")
org = "Dev"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Bitcoin"

influx_client = InfluxDBClient3(host=host, token=influx_token, org=org)
alpaca_client = CryptoDataStream(alpaca_key, alpaca_secret)


@dataclass
class Quote:
    symbol: str
    timestamp: datetime
    bid_price: float
    bid_size: float
    ask_price: float
    ask_size: float

    def to_point(self) -> Point:
        return (
            Point("btc_quotes")
            .tag("symbol", self.symbol)
            .field("bid_price", self.bid_price)
            .field("bid_size", self.bid_size)
            .field("ask_price", self.ask_price)
            .field("ask_size", self.ask_size)
            .time(self.timestamp)
        )


@dataclass
class Bar:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: float
    vwap: float

    def to_point(self) -> Point:
        return (
            Point("btc_bars")
            .tag("symbol", self.symbol)
            .field("open", self.open)
            .field("high", self.high)
            .field("low", self.low)
            .field("close", self.close)
            .field("volume", self.volume)
            .field("trade_count", self.trade_count)
            .field("vwap", self.vwap)
            .time(self.timestamp)
        )


async def quote_handler(data):
    quote = Quote(
        symbol=data.symbol,
        timestamp=data.timestamp,
        bid_price=data.bid_price,
        bid_size=data.bid_size,
        ask_price=data.ask_price,
        ask_size=data.ask_size
    )

    point = quote.to_point()
    influx_client.write(database=database, record=point)
    print(f"Wrote {data} to Quotes DB")


async def bar_handler(data):
    bar = Bar(
        symbol=data.symbol,
        timestamp=data.timestamp,
        open=data.open,
        high=data.high,
        low=data.low,
        close=data.close,
        volume=data.volume,
        trade_count=data.trade_count,
        vwap=data.vwap
    )

    point = bar.to_point()
    influx_client.write(database=database, record=point)
    print(f"Wrote {data} to Bars DB")

alpaca_client.subscribe_bars(bar_handler, "BTC/USD")
alpaca_client.subscribe_quotes(quote_handler, "BTC/USD")
alpaca_client.run()
