import json
from pathlib import Path


SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

# TD09 decision: the lab runs in APPROVED_SAMPLE mode.
ACCESS_MODE = "APPROVED_SAMPLE"

# Canonical MarketPulse ticker -> Bloomberg identifier
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def load_sample():
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        return json.load(file)


def normalize_bloomberg_history(series, canonical_ticker):
    rows = []

    for observation in series["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    data = load_sample()

    for series in data["series"]:
        if series["canonical_ticker"] == canonical_ticker:
            return normalize_bloomberg_history(series, canonical_ticker)

    raise ValueError(
        f"No approved Bloomberg sample for {canonical_ticker}"
    )