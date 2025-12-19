import datetime
import re
from typing import List

from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from fastapi import HTTPException


def parse_epoch_millis(epoch_ms: int) -> datetime.datetime:
    """Convert epoch milliseconds to a timezone-aware datetime (UTC)."""
    try:
        # Convert milliseconds to seconds and create UTC datetime
        return datetime.datetime.fromtimestamp(epoch_ms / 1000.0, tz=datetime.timezone.utc)
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=400, detail=f"Invalid epoch milliseconds: {epoch_ms}") from exc


def parse_timeframe(value: str) -> TimeFrame:
    """Convert strings like '1Day', '1Hour', '15Min' into an Alpaca TimeFrame."""
    match = re.fullmatch(
        r"(\d+)\s*(min|minute|minutes|hour|hours|day|days|week|weeks)", value, re.IGNORECASE)
    if not match:
        raise HTTPException(
            status_code=400, detail="timeframe must look like '1Day', '1Hour', or '15Min'.")

    amount = int(match.group(1))
    unit = match.group(2).lower()

    if "min" in unit:
        tf_unit = TimeFrameUnit.Minute
    elif "hour" in unit:
        tf_unit = TimeFrameUnit.Hour
    elif "day" in unit:
        tf_unit = TimeFrameUnit.Day
    else:
        tf_unit = TimeFrameUnit.Week

    return TimeFrame(amount, tf_unit)


def bars_to_response(df) -> List[dict]:
    """Normalize the Alpaca bar dataframe into a JSON-friendly list with single-letter field names."""
    if df.empty:
        return []
    records = []
    normalized = df.reset_index()
    for _, row in normalized.iterrows():
        timestamp = row.get("timestamp")
        # Convert timestamp to epoch milliseconds
        if hasattr(timestamp, 'timestamp'):
            # Pandas Timestamp objects
            epoch_seconds = timestamp.timestamp()
        elif isinstance(timestamp, datetime.datetime):
            # Ensure timezone-aware
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
            epoch_seconds = timestamp.timestamp()
        else:
            # Fallback: try to convert
            try:
                if hasattr(timestamp, 'value'):
                    # Pandas Timestamp nanoseconds, convert to seconds
                    epoch_seconds = timestamp.value / 1_000_000_000.0
                else:
                    epoch_seconds = float(timestamp)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=500, detail=f"Unable to convert timestamp: {timestamp}")

        # Convert to milliseconds (int64)
        epoch_millis = int(epoch_seconds * 1000)

        records.append(
            {
                "t": epoch_millis,
                "o": float(row.get("open")),
                "h": float(row.get("high")),
                "l": float(row.get("low")),
                "c": float(row.get("close")),
            }
        )
    return records
