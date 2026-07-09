# Algo

Tools for trading Indian markets.

- **`index.html`** - Nifty Algo Desk, a single-file browser dashboard for
  NIFTY/BankNifty/NSE watchlists: live signals (ORB + EMA-cross on 5-min
  candles), a paper-trading journal, and an equity-curve dashboard. Open it
  directly or host it on GitHub Pages; no build step.
- **`data/`** - Daily OHLCV history for NIFTY 50, NIFTY Bank, SENSEX and
  NIFTY 50 constituents, fetched from Yahoo Finance and refreshed by
  `.github/workflows/update-market-data.yml`. See `data/README.md`.
- **`scripts/fetch_market_data.py`** - the fetch script backing `data/`.

## Data pipeline quickstart

```
pip install -r requirements.txt
python scripts/fetch_market_data.py
```
