import pytest

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


@pytest.fixture
def prices():
    return [
        {"date": "2026-09-01", "ticker": "AAPL", "close": 100.0},
        {"date": "2026-09-02", "ticker": "AAPL", "close": 105.0},
        {"date": "2026-09-03", "ticker": "AAPL", "close": 110.0},
    ]


def test_period_return_known_value(prices):
    assert calculate_period_return(prices) == pytest.approx(10.0)


def test_base_100_starts_at_100(prices):
    result = calculate_base_100(prices)
    assert len(result) == len(prices)
    assert result[0]["value"] == pytest.approx(100.0)
    assert result[-1]["value"] == pytest.approx(110.0)


@pytest.mark.parametrize(
    "instrument, benchmark, expected",
    [(6.48, 2.15, 4.33), (2.0, 5.0, -3.0), (1.5, 1.5, 0.0)],
)
def test_relative_performance(instrument, benchmark, expected):
    result = calculate_relative_performance(instrument, benchmark)
    assert result == pytest.approx(expected)


def test_align_series_keeps_only_common_dates():
    a = [{"date": d, "close": 1.0} for d in ["2026-09-01", "2026-09-02", "2026-09-03"]]
    b = [{"date": d, "close": 2.0} for d in ["2026-09-02", "2026-09-03", "2026-09-04"]]
    aligned_a, aligned_b = align_series(a, b)
    assert [row["date"] for row in aligned_a] == ["2026-09-02", "2026-09-03"]
    assert len(aligned_a) == len(aligned_b)