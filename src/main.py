from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    ACCESS_MODE as BLOOMBERG_ACCESS_MODE,
    fetch_bloomberg_prices,
)
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
DATA_SOURCE = "bloomberg"  # "bloomberg", "yahoo" or "csv"
PROVIDER_LABELS = {
    "bloomberg": "Bloomberg stage",
    "yahoo": "Yahoo Finance via yfinance",
    "csv": "CSV",
}
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def load_csv_series(instrument, benchmark):
    normalized_prices = [
        normalize_price_row(row)
        for row in load_prices()
    ]
    instrument_prices = filter_prices(normalized_prices, instrument["ticker"])
    benchmark_prices = filter_prices(normalized_prices, benchmark["ticker"])
    return instrument_prices, benchmark_prices


def load_yahoo_series(instrument, benchmark):
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )
    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )
    return instrument_prices, benchmark_prices


def load_bloomberg_series(instrument, benchmark):
    instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
    benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])
    return instrument_prices, benchmark_prices


def load_series(data_source, instrument, benchmark):
    if data_source == "bloomberg":
        return load_bloomberg_series(instrument, benchmark)
    if data_source == "yahoo":
        return load_yahoo_series(instrument, benchmark)
    return load_csv_series(instrument, benchmark)


def get_access_mode(data_source):
    if data_source == "bloomberg":
        return BLOOMBERG_ACCESS_MODE
    return None


def build_market_snapshot(data_source=DATA_SOURCE):
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices, benchmark_prices = load_series(
        data_source,
        instrument,
        benchmark,
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        raise ValueError("No common dates between instrument and benchmark")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": PROVIDER_LABELS[data_source],
        "access_mode": get_access_mode(data_source),
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": aligned_instrument,
        "benchmark_prices": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return,
            benchmark_return,
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def display_market_summary(asset, prices, period_return, show_currency=True):
    first_close = prices[0]["close"]
    last_close = prices[-1]["close"]

    if show_currency:
        currency = f" {asset['currency']}"
    else:
        currency = ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Currency      : {asset['currency']}")
    print(f"Market        : {asset['market']}")
    print(f"Observations  : {len(prices)}")
    print(f"First date    : {prices[0]['date']}")
    print(f"Last date     : {prices[-1]['date']}")
    print(f"First close   : {first_close:.2f}{currency}")
    print(f"Last close    : {last_close:.2f}{currency}")
    print(f"Period return : {period_return:.2f}%")


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider    : {snapshot['provider']}")
    if snapshot["access_mode"]:
        print(f"Access mode : {snapshot['access_mode']}")
    print(f"Period      : {snapshot['lookback']}")
    print(f"Interval    : {snapshot['interval']}")
    print()
    print("Instrument")
    display_market_summary(
        instrument,
        snapshot["instrument_prices"],
        snapshot["instrument_return"],
    )
    print()
    print("Benchmark")
    display_market_summary(
        benchmark,
        snapshot["benchmark_prices"],
        snapshot["benchmark_return"],
        show_currency=False,
    )
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
