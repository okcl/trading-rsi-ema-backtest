
import pandas as pd
from strategy.rsi_ema_strategy import generate_rsi_ema_signals
import os

def run_backtest(csv_path, initial_balance=1000):
    df = generate_rsi_ema_signals(csv_path)

    balance = initial_balance
    position = 0
    entry_price = 0
    trades = []

    for index, row in df.iterrows():
        price = row['close']
        signal = row['signal']
        timestamp = row['timestamp']

        if signal == 'BUY' and position == 0:
            position = balance / price
            entry_price = price
            balance = 0
            trades.append({'timestamp': timestamp, 'type': 'BUY', 'price': price, 'balance': 0})

        elif signal == 'SELL' and position > 0:
            balance = position * price
            profit = balance - (entry_price * position)
            trades.append({'timestamp': timestamp, 'type': 'SELL', 'price': price, 'balance': balance, 'profit': profit})
            position = 0

    if position > 0:
        balance = position * df.iloc[-1]['close']
        trades.append({'timestamp': df.iloc[-1]['timestamp'], 'type': 'FORCED SELL', 'price': df.iloc[-1]['close'], 'balance': balance})

    trades_df = pd.DataFrame(trades)
    os.makedirs("logs", exist_ok=True)
    trades_df.to_csv("logs/trades.csv", index=False)

    total_profit = balance - initial_balance
    stats = {
        "initial_balance": initial_balance,
        "final_balance": balance,
        "total_profit": total_profit,
        "num_trades": len(trades_df) // 2
    }

    return stats