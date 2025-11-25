FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY stock_app.py .

# Default envs (can be overridden at runtime)
ENV TICKERS="MSFT,NVDA,GOOGL,META,AMZN,APPL,ADBE,AVGO,AMD,TSMC,ASML,C,JPM,TSLA,NIO,ARE,RIO,UPS"
ENV INTERVAL_SECONDS="60"
ENV PERCENT_CHANGE_ALERT="2.0"
ENV STATE_FILE="last_prices.json"

CMD ["python", "stock_app.py"]