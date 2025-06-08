import pandas as pd
import ta

def generate_rsi_ema_signals(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    # RSI ve EMA'lar
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    df['ema_fast'] = ta.trend.EMAIndicator(close=df['close'], window=10).ema_indicator()
    df['ema_slow'] = ta.trend.EMAIndicator(close=df['close'], window=21).ema_indicator()

    # Esnek sinyal kuralları
    df['signal'] = 'HOLD'
    position = None  # işlemde misin değil misin kontrolü

    for i in range(1, len(df)):
        rsi = df.at[i, 'rsi']
        ema_fast = df.at[i, 'ema_fast']
        ema_slow = df.at[i, 'ema_slow']
        prev_ema_fast = df.at[i - 1, 'ema_fast']
        prev_ema_slow = df.at[i - 1, 'ema_slow']

        # Daha esnek eşikler
        if position != 'LONG' and rsi > 55 and prev_ema_fast < prev_ema_slow and ema_fast > ema_slow:
            df.at[i, 'signal'] = 'BUY'
            position = 'LONG'

        elif position == 'LONG' and (rsi < 45 or ema_fast < ema_slow):
            df.at[i, 'signal'] = 'SELL'
            position = None

    return df
