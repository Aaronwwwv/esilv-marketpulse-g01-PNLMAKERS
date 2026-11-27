from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    ACCESS_MODE,
    fetch_bloomberg_prices,
)


DATA_DIR = Path("data/sample")

PROVIDER_LABEL = "Bloomberg stage"
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot(instruments):
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
    benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": PROVIDER_LABEL,
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "aligned_instrument": aligned_instrument,
        "aligned_benchmark": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return,
            benchmark_return,
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def print_series_summary(asset, prices, period_return):
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations  : {len(prices)}")
    print(f"First date    : {prices[0]['date']}")
    print(f"Last date     : {prices[-1]['date']}")
    print(f"Period return : {period_return:.2f}%")


def main():
    instruments = load_instruments()
    snapshot = build_market_snapshot(instruments)

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider    : {snapshot['provider']}")
    print(f"Access mode : {snapshot['access_mode']}")
    print(f"Period      : {snapshot['lookback']}")
    print(f"Interval    : {snapshot['interval']}")
    print()
    print("Instrument")
    print_series_summary(
        instrument,
        snapshot["aligned_instrument"],
        snapshot["instrument_return"],
    )
    print()
    print("Benchmark")
    print_series_summary(
        benchmark,
        snapshot["aligned_benchmark"],
        snapshot["benchmark_return"],
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
        f"{snapshot['instrument_base_100'][0]['value']:.2f} -> "
        f"{snapshot['instrument_base_100'][-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{snapshot['benchmark_base_100'][0]['value']:.2f} -> "
        f"{snapshot['benchmark_base_100'][-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()