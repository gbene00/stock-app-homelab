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
    return {
        "tickers": tickers,
        "prices": get_current_prices(tickers),
    }


@app.get("/healthz")
def health():
    return {"status": "ok"}