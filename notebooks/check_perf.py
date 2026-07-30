import requests
import time

tickers = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK"
]

for ticker in tickers:

    start = time.time()

    r = requests.get(
        f"http://127.0.0.1:8000/api/v1/companies/{ticker}"
    )

    elapsed = round(
        time.time() - start,
        3
    )

    print(
        ticker,
        elapsed,
        "sec",
        r.status_code
    )