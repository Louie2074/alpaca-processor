# FinanceBot Data API

A FastAPI REST API for retrieving historical stock market data using the Alpaca API.

## Features

- **Historical Stock Data**: Retrieve historical bar data for stocks
- **Multiple Symbols**: Query data for one or multiple stock symbols at once
- **Flexible Timeframes**: Support for various timeframes (1Day, 1Hour, 15Min, etc.)
- **Epoch Milliseconds**: Simple timestamp format using epoch milliseconds

## Setup

1. Create and activate virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   Create a `.env` file with:

```
ALPACA_KEY=your-key
ALPACA_SECRET=your-secret
```

## Running the Application

### Option 1: Direct execution

```bash
python app.py
```

### Option 2: Using uvicorn (with auto-reload)

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/stocks/bars`

Retrieve historical stock bar data.

**Query Parameters:**
- `symbols` (required, array): Stock symbol(s) to query (e.g., `AAPL`, `MSFT`)
- `timeframe` (required, string): Timeframe for bars (e.g., `1Day`, `1Hour`, `15Min`)
- `start` (required, int): Start time as epoch milliseconds (e.g., `1704067200000`)
- `end` (required, int): End time as epoch milliseconds (e.g., `1704153600000`)

**Example Requests:**

Single symbol:
```bash
curl "http://localhost:8000/stocks/bars?symbols=AAPL&timeframe=1Day&start=1704067200000&end=1704153600000"
```

Multiple symbols:
```bash
curl "http://localhost:8000/stocks/bars?symbols=AAPL&symbols=MSFT&symbols=GOOGL&timeframe=1Hour&start=1704067200000&end=1704153600000"
```

**Response Format:**
Returns an array of bar objects:
```json
[
  {
    "t": 1704067200000,
    "o": 150.25,
    "h": 151.50,
    "l": 149.75,
    "c": 150.80,
    "v": 1000000,
    "n": 5000,
    "vw": 150.50
  }
]
```

Where:
- `t`: Timestamp in epoch milliseconds
- `o`: Opening price
- `h`: High price
- `l`: Low price
- `c`: Closing price
- `v`: Volume
- `n`: Trade count
- `vw`: Volume weighted average price

### GET `/health`

Health check endpoint.

```bash
curl http://localhost:8000/health
```

Returns: `{"status": "ok"}`

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Getting Epoch Milliseconds

To get the current epoch milliseconds in milliseconds:

```bash
python3 -c "import time; print(int(time.time() * 1000))"
```

Or using date command:
```bash
echo $(($(date +%s) * 1000))
```

## Deployment

1. Set Fly.io secrets:

```bash
fly secrets set ALPACA_KEY="your-key"
fly secrets set ALPACA_SECRET="your-secret"
```

2. Deploy to Fly.io:

```bash
fly deploy
```
