import os
from typing import List

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

from utils import bars_to_response, parse_epoch_millis, parse_timeframe

load_dotenv()

ALPACA_KEY = os.getenv("ALPACA_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")

if not ALPACA_KEY or not ALPACA_SECRET:
    raise RuntimeError(
        "ALPACA_KEY and ALPACA_SECRET environment variables are required.")

stock_client = StockHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)
app = FastAPI(title="FinanceBot Data API")


@app.get("/stocks/bars")
async def get_stock_bars(
    symbols: List[str] = Query(..., min_length=1),
    timeframe: str = Query(..., description="Examples: 1Day, 1Hour, 15Min"),
    start: int = Query(...,
                       description="Start time as epoch milliseconds (e.g. 1704067200000)"),
    end: int = Query(...,
                     description="End time as epoch milliseconds (e.g. 1704153600000)"),
):
    """
    Get historical stock bar data.

    Example URLs:
        Single symbol:
        /stocks/bars?symbols=AAPL&timeframe=1Day&start=1704067200000&end=1766185583116

        Multiple symbols:
        /stocks/bars?symbols=AAPL&symbols=MSFT&symbols=GOOGL&timeframe=1Hour&start=1704067200000&end=1765235227

    Returns an array of bar objects with fields: t (timestamp in epoch ms), o (open), h (high), 
    l (low), c (close), v (volume), n (trade count), vw (volume weighted average price).
    """
    tf = parse_timeframe(timeframe)
    start_dt = parse_epoch_millis(start)
    end_dt = parse_epoch_millis(end)

    request = StockBarsRequest(
        symbol_or_symbols=symbols, timeframe=tf, start=start_dt, end=end_dt)
    try:
        bars = stock_client.get_stock_bars(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return bars_to_response(bars.df)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
