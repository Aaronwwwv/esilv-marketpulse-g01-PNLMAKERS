
# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (not present in the team repository at the time of TD09; the mapping below was derived by comparing the sample fixture with `data/sample/bloomberg_reference_expected.json`)
- Live connectivity: not demonstrated
- The fixture itself declares `"access_mode": "approved_sample"` and `"is_live_bloomberg_output": false`.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The canonical tickers (AAPL, SP500) are preserved in MarketPulse rows.
Bloomberg identifiers are used only at the provider boundary.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key; string `YYYY-MM-DD` |
| ticker | application mapping from `canonical_ticker` | AAPL or SP500 (never the Bloomberg identifier) |
| open | `open_value` | teaching wrapper key; number |
| high | `high_value` | teaching wrapper key; number |
| low | `low_value` | teaching wrapper key; number |
| close | `close_value` | teaching wrapper key; number |
| volume | `volume_value` | teaching wrapper key; integer; `0` for SP500 |

Important: teaching wrapper key != Bloomberg LIVE field mnemonic.
The `*_value` / `observation_date` keys come from the approved fallback fixture
(see its `schema_note`). No LIVE Bloomberg field name was observed in this session,
so none is documented here.

## Observations

- Instrument series: `AAPL US Equity`, canonical ticker `AAPL`, 21 observations.
- Benchmark series: `SPX Index`, canonical ticker `SP500`, 21 observations.
- First observation date: 2026-09-01 for both series.
- Null values found in the fixture: 0.
- Values are illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg historical observations.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity -> canonical ticker AAPL
- Benchmark identifier: SPX Index -> canonical ticker SP500
- Date representation: string `YYYY-MM-DD` in `observation_date`
- Input structure: JSON object with a `series` list; each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list
- Missing fields: none in the fixture (0 null values)
- Special normalization notes:
  - set `ticker` from `canonical_ticker`, not from `provider_identifier`
  - convert `open_value` / `high_value` / `low_value` / `close_value` with `float()` (some values are written without decimals, e.g. `248`)
  - convert `volume_value` with `int()`; SP500 volume is `0`
  - output must be canonical rows usable by the existing `analytics.py` without change
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
