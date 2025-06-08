import requests
import pandas as pd
import time
from datetime import datetime, timedelta

def fetch_klines(symbol="BTCUSDT", interval="5m", days=1, save_path="data/btc_usdt_5m.csv"):
    end_time = int(time.time() * 1000)
    start_time = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)

    url = "https://api.binance.com/api/v3/klines"
    limit = 1000  # Binance API en fazla 1000 veri döner
    all_data = []

    while start_time < end_time:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            break

        all_data += data
        last_time = data[-1][0]
        start_time = last_time + 1  # Çakışma olmasın diye 1 ms ekle

        time.sleep(0.1)

    df = pd.DataFrame(all_data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    df = df[["timestamp", "close"]]

    df.to_csv(save_path, index=False)
    print(f"Veri kaydedildi: {save_path}")
