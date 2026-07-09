# Indian stock market data

Daily OHLCV history for major Indian indices and NIFTY 50 constituents,
sourced from Yahoo Finance.

## Layout

```
data/
  indices/    NIFTY50.csv, NIFTYBANK.csv, SENSEX.csv
  nifty50/    one CSV per NIFTY 50 constituent, e.g. RELIANCE.csv, TCS.csv
```

Each CSV has columns: `Date, Open, High, Low, Close, Adj Close, Volume`.

## Refreshing the data

```
pip install -r requirements.txt
python scripts/fetch_market_data.py            # 5 years, indices + constituents
python scripts/fetch_market_data.py --years 1  # shorter window
python scripts/fetch_market_data.py --only-indices
```

The `.github/workflows/update-market-data.yml` workflow runs this script
automatically on weekday afternoons (after NSE close) and commits any
changes, so `data/` stays current without a manual run.

## Notes

- Symbols use Yahoo Finance's NSE convention (`.NS` suffix); indices use
  `^NSEI` (NIFTY 50), `^NSEBANK` (NIFTY Bank), `^BSESN` (SENSEX).
- The NIFTY 50 constituent list in `scripts/fetch_market_data.py` reflects
  the index composition at the time it was written and drifts as NSE
  rebalances the index — cross-check against nseindia.com if you need an
  authoritative list.
