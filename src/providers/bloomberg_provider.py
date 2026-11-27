import json
from pathlib import Path


ACCESS_MODE = "APPROVED_SAMPLE"
SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

# Canonical MarketPulse ticker -> Bloomberg identifier (TD09 mapping)
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    # APPROVED_SAMPLE raw input boundary: reads the approved fallback fixture.
    # No live Bloomberg connection is made here.
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        fixture = json.load(file)

    for series in fixture["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"No approved sample series for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    # Teaching wrapper keys (not Bloomberg field mnemonics) -> canonical row
    rows = []

    for observation in raw_data["observations"]:
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
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)

    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError(
            f"Sample series {identifier} is not mapped to {canonical_ticker}"
        )

    rows = normalize_bloomberg_history(raw_data, canonical_ticker)

    if not rows:
        raise ValueError(f"No Bloomberg-stage rows for {canonical_ticker}")

    return rows
