#!/usr/bin/env python3
"""Fetch daily OHLCV history for Indian stock market indices and NIFTY 50
constituents from Yahoo Finance and save it as CSV under data/.

Usage:
    pip install -r requirements.txt
    python scripts/fetch_market_data.py [--years 5] [--only-indices]
"""
import argparse
import sys
import time
from pathlib import Path

import yfinance as yf

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

INDICES = {
    "^NSEI": "NIFTY50",
    "^NSEBANK": "NIFTYBANK",
    "^BSESN": "SENSEX",
}

# NIFTY 50 constituents, Yahoo Finance NSE tickers (.NS suffix).
# Index composition changes periodically - verify against nseindia.com
# before relying on this list for anything beyond sampling.
NIFTY50_CONSTITUENTS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
    "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BEL.NS", "BHARTIARTL.NS", "CIPLA.NS", "COALINDIA.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS",
    "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", "INDUSINDBK.NS",
    "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS",
    "SHRIRAMFIN.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS",
    "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
    "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "UPL.NS",
    "WIPRO.NS",
]


def fetch_symbol(symbol: str, filename: str, period: str, out_dir: Path) -> bool:
    try:
        df = yf.download(symbol, period=period, interval="1d",
                          auto_adjust=False, progress=False)
    except Exception as exc:
        print(f"  ! {symbol}: {exc}", file=sys.stderr)
        return False
    if df.empty:
        print(f"  ! {symbol}: no data returned", file=sys.stderr)
        return False
    df.index.name = "Date"
    df.reset_index(inplace=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / f"{filename}.csv", index=False)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", type=int, default=5,
                         help="years of daily history to fetch (default: 5)")
    parser.add_argument("--only-indices", action="store_true",
                         help="skip individual stock constituents")
    args = parser.parse_args()
    period = f"{args.years}y"

    ok = fail = 0
    print("Fetching indices...")
    for symbol, name in INDICES.items():
        if fetch_symbol(symbol, name, period, DATA_DIR / "indices"):
            ok += 1
        else:
            fail += 1
        time.sleep(0.5)

    if not args.only_indices:
        print("Fetching NIFTY 50 constituents...")
        for symbol in NIFTY50_CONSTITUENTS:
            name = symbol.replace(".NS", "")
            if fetch_symbol(symbol, name, period, DATA_DIR / "nifty50"):
                ok += 1
            else:
                fail += 1
            time.sleep(0.5)

    print(f"Done: {ok} succeeded, {fail} failed.")
    sys.exit(1 if fail and not ok else 0)


if __name__ == "__main__":
    main()
