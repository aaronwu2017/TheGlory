"""Download ATOM spot data from Binance, Coinbase, Gemini"""
from tardis_dev import datasets
import logging
import os
import pandas as pd
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

logging.basicConfig(level=logging.DEBUG)

EXCHANGES = ["binance", "coinbase", "gemini"]

SYMBOL_MAP = {
    "binance": ["ATOMUSDT"],
    "coinbase": ["ATOM-USD"],
    "gemini": ["ATOMUSD"],
}

def download_atom_spot():
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Downloading ATOM spot data...")

    for exchange in EXCHANGES:
        symbols = SYMBOL_MAP.get(exchange, [])
        for symbol in symbols:
            try:
                print(f"\n--- Downloading {exchange} {symbol} ---")
                datasets.download(
                    exchange=exchange,
                    data_types=["trades"],
                    from_date="2025-10-10",
                    to_date="2025-10-11",
                    symbols=[symbol],
                    api_key=api_key,
                    download_dir=os.path.join(script_dir, exchange)
                )
                print(f"✓ {exchange} {symbol} completed!")
            except Exception as e:
                print(f"✗ Error: {exchange} {symbol}: {e}")

def analyze_prices():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("\n=== ATOM SPOT PRICE ANALYSIS ===\n")
    
    for exchange in EXCHANGES:
        exchange_dir = os.path.join(script_dir, exchange)
        if os.path.exists(exchange_dir):
            for file in os.listdir(exchange_dir):
                if file.endswith('.csv') or file.endswith('.csv.gz'):
                    try:
                        df = pd.read_csv(os.path.join(exchange_dir, file))
                        if 'price' in df.columns:
                            min_price = df['price'].min()
                            max_price = df['price'].max()
                            print(f"{exchange.upper():12} | Min: {min_price:.4f} | Max: {max_price:.2f}")
                    except Exception as e:
                        print(f"Error: {exchange} - {e}")

if __name__ == "__main__":
    download_atom_spot()
    analyze_prices()
