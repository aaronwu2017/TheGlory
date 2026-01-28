import pandas as pd
import os

download_dir = r'C:\Users\aaron\OneDrive\Desktop\黑暗荣耀1011\analysis\spot\coin_margined'
results = {}

for file in os.listdir(download_dir):
    if file.endswith('.csv.gz'):
        filepath = os.path.join(download_dir, file)
        try:
            df = pd.read_csv(filepath)
            if 'price' in df.columns:
                min_price = df['price'].min()
                max_price = df['price'].max()
                symbol = file.replace('binance-delivery_trades_2025-10-10_', '').replace('.csv.gz', '')
                coin = symbol.replace('USD_PERP', '')
                results[coin] = {'min': min_price, 'max': max_price}
        except Exception as e:
            print(f'Error: {file} - {e}')

print("=== COIN-MARGINED FUTURES MIN PRICES ===\n")
print(f"{'Coin':<8} | {'Min Price':>15} | {'Max Price':>12} | {'Drop %':>8}")
print("-" * 55)

for coin in sorted(results.keys()):
    data = results[coin]
    drop = ((data['max'] - data['min']) / data['max']) * 100
    print(f"{coin:<8} | {data['min']:>15.6f} | {data['max']:>12.2f} | {drop:>7.1f}%")
