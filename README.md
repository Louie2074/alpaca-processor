# Finance Bot

A Python application for streaming and processing cryptocurrency data.

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
ALPACA_KEY = "your-key"
ALPACA_SECRET = "your-secret"
INFLUXDB_TOKEN = "your-token"
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:

```bash
python app.py
```

## Deployment

1. Set Fly.io secrets:

```bash
fly secrets set ALPACA_KEY="your-key"
fly secrets set ALPACA_SECRET="your-secret"
fly secrets set INFLUXDB_TOKEN="your-token"
```

2. Deploy to Fly.io:

```bash
fly deploy
```
