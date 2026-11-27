import pytest

from analytics import calculate_base_100, calculate_period_return


def test_calculate_period_return():
    prices = [
        {"date": "2026-01-01", "ticker": "TEST", "close": 100.0},
        {"date": "2026-01-02", "ticker": "TEST", "close": 110.0},
    ]

    assert calculate_period_return(prices) == pytest.approx(10.0)


def test_calculate_base_100_starts_at_100():
    prices = [
        {"date": "2026-01-01", "ticker": "TEST", "close": 50.0},
        {"date": "2026-01-02", "ticker": "TEST", "close": 75.0},
    ]

    result = calculate_base_100(prices)

    assert result[0]["value"] == 100.0
    assert result[-1]["value"] == pytest.approx(150.0)
    