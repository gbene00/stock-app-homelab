FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stock_app.py api.py .

# Default envs (can be overridden at runtime)
ENV TICKERS="MSFT,NVDA,GOOGL,META,AMZN,APPL,ADBE,AVGO,AMD,TSMC,ASML,C,JPM,TSLA,NIO,ARE,RIO,UPS"
ENV INTERVAL_SECONDS="60"
ENV PERCENT_CHANGE_ALERT="2.0"
ENV STATE_FILE="last_prices.json"

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]