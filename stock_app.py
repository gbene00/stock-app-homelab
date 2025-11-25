import os
import time
import json
from typing import Dict, List

import yfinance as yf


def load_last_prices(path: str) -> Dict[str, float]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        # If file is corrupted or unreadable, start fresh
        return {}


def save_last_prices(path: str, prices: Dict[str, float]) -> None:
    with open(path, "w") as f:
        json.dump(prices, f)


def get_current_price(ticker: str) -> float | None:
    """
    Fetch the latest close price for a single ticker.
    Returns None if it can't get a price.
    """
    try:
        t = yf.Ticker(ticker)
        # Try intraday first
        data = t.history(period="1d", interval="1m")
        if data.empty:
            # Fallback to daily
            data = t.history(period="1d")
        if data.empty:
            return None
        last_row = data.tail(1)
        return float(last_row["Close"].iloc[0])
    except Exception:
        return None


def get_current_prices(tickers: List[str]) -> Dict[str, float]:
    prices: Dict[str, float] = {}
    for t in tickers:
        price = get_current_price(t)
        if price is not None:
            prices[t] = price
    return prices


def main() -> None:
    # Config from environment
    tickers_env = os.getenv("TICKERS", "MSFT,AAPL")
    tickers = [t.strip().upper() for t in tickers_env.split(",") if t.strip()]

    interval_seconds = int(os.getenv("INTERVAL_SECONDS", "60"))
    alert_percent = float(os.getenv("PERCENT_CHANGE_ALERT", "2.0"))
    state_file = os.getenv("STATE_FILE", "last_prices.json")

    print(f"Starting stock watcher for: {tickers}")
    print(f"Check interval: {interval_seconds}s, alert threshold: {alert_percent}%")
    print(f"State file: {state_file}")
    print("-" * 60)

    last_prices = load_last_prices(state_file)

    while True:
        try:
            current_prices = get_current_prices(tickers)
            if not current_prices:
                print("No prices fetched, will retry...")
            for ticker, current_price in current_prices.items():
                # store with only 2 decimals
                rounded_price = round(current_price, 2)

                last_price = last_prices.get(ticker)
                if last_price is None:
                    print(f"[INIT] {ticker}: current price {rounded_price:.2f}")
                else:
                    change = rounded_price - last_price
                    change_pct = (change / last_price) * 100 if last_price != 0 else 0

                    if abs(change_pct) >= alert_percent:
                        direction = "UP" if change_pct > 0 else "DOWN"
                        print(
                            f"[ALERT] {ticker}: {direction} "
                            f"{change_pct:.2f}% | "
                            f"was {last_price:.2f}, now {rounded_price:.2f}"
                        )
                    else:
                        print(
                            f"[INFO] {ticker}: change {change_pct:.2f}% | "
                            f"last {last_price:.2f}, now {rounded_price:.2f}"
                        )

                # update last price (2 decimals)
                last_prices[ticker] = rounded_price

            save_last_prices(state_file, last_prices)

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()