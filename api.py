import os
from typing import List

from fastapi import FastAPI
from stock_app import get_current_prices  # reuse your existing logic

app = FastAPI()


def get_tickers_from_env() -> List[str]:
    tickers_env = os.getenv(
        "TICKERS",
        "MSFT,AAPL",
    )
    return [t.strip().upper() for t in tickers_env.split(",") if t.strip()]


@app.get("/prices")
def read_prices():
    tickers = get_tickers_from_env()
    raw_prices = get_current_prices(tickers)

    stocks = []
    for t in tickers:
        price = raw_prices.get(t)
        if price is not None:
            stocks.append(
                {
                    "ticker": t,
                    # price as string with exactly 2 decimals
                    "price": f"{round(price, 2):.2f}",
                }
            )

    return {
        "count": len(stocks),
        "stocks": stocks,
    }

@app.get("/healthz")
def health():
    return {"status": "ok"}