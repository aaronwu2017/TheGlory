from tardis_dev import datasets
import logging
import os
import pandas as pd
import sys

# Handle console encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

logging.basicConfig(level=logging.INFO)

API_KEY = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"

COINS = [
    "ETH", "XRP", "BNB", "ADA", "DOT", "LINK", "LTC", "BCH", "FIL", "UNI", "AVAX", "ETC", "TRX", "XLM"
]

EXCHANGES = ["binance", "coinbase", "gemini"]

# Symbol mappings
def get_symbol(exchange, coin):
    if exchange == "binance":
        return f"{coin}USDT"
    elif exchange == "coinbase":
        return f"{coin}-USD"
    elif exchange == "gemini":
        return f"{coin}USD"
    return None

def download_missing_spot():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir # analysis/spot
    
    results = {}

    for coin in COINS:
        print(f"\nProcessing {coin}...")
        results[coin] = {}
        
        for exchange in EXCHANGES:
            # Create coin/exchange directory
            download_dir = os.path.join(base_dir, coin, exchange)
            os.makedirs(download_dir, exist_ok=True)
            
            symbol = get_symbol(exchange, coin)
            
            # Check if likely already exists
            existing_files = [f for f in os.listdir(download_dir) if f.endswith('.csv') or f.endswith('.csv.gz')]
            if existing_files:
                print(f"  {exchange}: Data already exists for {coin}")
            else:
                print(f"  {exchange}: Downloading {symbol}...")
                try:
                    datasets.download(
                        exchange=exchange,
                        data_types=["trades"],
                        from_date="2025-10-10",
                        to_date="2025-10-11",
                        symbols=[symbol],
                        api_key=API_KEY,
                        download_dir=download_dir
                    )
                except Exception as e:
                    print(f"  {exchange}: Failed to download {symbol} - {e}")

            # Analyze immediately
            min_price = None
            existing_files = [f for f in os.listdir(download_dir) if f.endswith('.csv') or f.endswith('.csv.gz')]
            if existing_files:
                try:
                    df = pd.read_csv(os.path.join(download_dir, existing_files[0]))
                    if 'price' in df.columns and not df.empty:
                        min_price = df['price'].min()
                except Exception as e:
                    print(f"  {exchange}: Error reading data - {e}")
            
            results[coin][exchange] = min_price
            print(f"  {exchange} Min: {min_price}")

    print("\n=== SUMMARY TABLE DATA ===")
    print("Coin | Coinbase Min | Binance Spot | Gemini Spot")
    for coin in COINS:
        cb = results[coin].get('coinbase')
        bin = results[coin].get('binance')
        gem = results[coin].get('gemini')
        print(f"{coin} | {cb} | {bin} | {gem}")

if __name__ == "__main__":
    download_missing_spot()
