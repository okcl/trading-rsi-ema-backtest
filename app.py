import streamlit as st
from utils.fetch_binance_data import fetch_klines
from backtest.run_backtest import run_backtest
import pandas as pd
import os
import plotly.graph_objects as go

st.markdown("""
Bu dashboard, Binance'den seçilen zaman aralığı ve gün sayısına göre **BTCUSDT** verilerini indirip, 
RSI ve EMA göstergelerine dayalı basit bir alım-satım stratejisinin geçmiş performansını test eder.

**Strateji Özeti:**  
- RSI (Relative Strength Index) ile aşırı alım ve aşırı satım seviyeleri tespit edilir.  
- EMA (Exponential Moving Average) ile trend yönü belirlenir.  
- **Alış (BUY) sinyali:** RSI 55'in üzerinde ve hızlı EMA, yavaş EMA'yı aşağıdan yukarı keserse pozisyon açılır.  
- **Satış (SELL) sinyali:** Pozisyondayken RSI 45'in altına düşerse veya hızlı EMA, yavaş EMA'yı yukarıdan aşağı keserse pozisyon kapatılır.  
- Bu esnek kurallar, piyasa koşullarına uyumlu dengeli işlem yapılmasını sağlar.

Backtest sonucunda toplam kar, işlem sayısı ve bakiye değişimleri grafiklerle sunulur.

Veriyi indirip backtest yapmak için aşağıdaki butonu kullanabilirsiniz.
""")


# Seçimler
interval = st.selectbox("Zaman Aralığı", ["5m", "15m", "30m", "1h"])
days = st.number_input("Kaç günlük veri çekilsin?", min_value=1, max_value=30, value=3)

symbol = "BTCUSDT"
csv_path = f"data/btc_usdt_{interval}.csv"

if st.button("Veriyi İndir ve Backtest Yap"):

    st.info("Veri indiriliyor...")
    fetch_klines(symbol=symbol, interval=interval, days=days, save_path=csv_path)

    st.success("Veri indirildi. Backtest yapılıyor...")
    result = run_backtest(csv_path=csv_path)

    st.success("Backtest tamamlandı.")
    st.write(f"💰 Başlangıç Bakiyesi: ${result['initial_balance']:.2f}")
    st.write(f"📈 Bitiş Bakiyesi: ${result['final_balance']:.2f}")
    st.write(f"📊 Toplam Kâr: ${result['total_profit']:.2f}")
    st.write(f"🔁 Trade Sayısı: {result['num_trades']}")

    if os.path.exists("logs/trades.csv"):
        trades = pd.read_csv("logs/trades.csv", parse_dates=['timestamp'])

        st.subheader("Trade Noktaları")
        st.dataframe(trades)

        fig = go.Figure()

        # İşlem fiyatlarını çizgi olarak eklemek istersek:
        fig.add_trace(go.Scatter(x=trades['timestamp'], y=trades['price'], mode='lines', name='İşlem Fiyatı'))

        # Büyük harfli tiplere göre filtreleme yapalım
        buys = trades[trades['type'].str.upper() == 'BUY']
        sells = trades[trades['type'].str.upper() == 'SELL']
        forced_sells = trades[trades['type'].str.upper() == 'FORCED SELL']

        fig.add_trace(go.Scatter(
            x=buys['timestamp'], y=buys['price'], mode='markers', name='Buy',
            marker=dict(color='green', size=10, symbol='triangle-up')
        ))

        fig.add_trace(go.Scatter(
            x=sells['timestamp'], y=sells['price'], mode='markers', name='Sell',
            marker=dict(color='red', size=10, symbol='triangle-down')
        ))

        fig.add_trace(go.Scatter(
            x=forced_sells['timestamp'], y=forced_sells['price'], mode='markers', name='Forced Sell',
            marker=dict(color='orange', size=12, symbol='x')
        ))

        fig.update_layout(title='İşlem Fiyatları ve Al-Sat Noktaları', xaxis_title='Zaman', yaxis_title='Fiyat')
        st.plotly_chart(fig)
