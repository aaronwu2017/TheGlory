from tardis_dev import datasets
import logging
import os
import pandas as pd
import sys

# Handle console encoding on Windows for non-ASCII paths
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Configure logging to see download progress
logging.basicConfig(level=logging.DEBUG)

# Target exchanges: Binance baseline + Coinbase, Gemini
EXCHANGES = [
    "binance",
    "coinbase",
    "gemini",
]

# Exchange-specific DOGE/USD symbol mapping
SYMBOL_MAP = {
    "binance": ["DOGEUSDT"],
    "coinbase": ["DOGE-USD"],
    "gemini": ["DOGEUSD"],
}

def download_spot_trades():
    """
    Downloads DOGE spot trading data across major exchanges for 2025-10-10.
    """
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"

    # Store data alongside this script (per coin)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = script_dir
    os.makedirs(download_dir, exist_ok=True)

    print("Starting DOGE spot trade data downloads...")
    print(f"Saving to: {download_dir}")
    print(f"Target exchanges: {', '.join(EXCHANGES)}")
    print(f"Using API Key: {api_key[:5]}... (Check if this key has access to the requested dates)")

    for exchange in EXCHANGES:
        exchange_symbols = SYMBOL_MAP.get(exchange, ["DOGEUSDT"])
        success = 0
        print(f"\n--- Downloading {exchange.upper()} spot trades ---")
        for symbol in exchange_symbols:
            try:
                datasets.download(
                    exchange=exchange,
                    data_types=["trades"],
                    from_date="2025-10-10",
                    to_date="2025-10-11",
                    symbols=[symbol],
                    api_key=api_key,
                    download_dir=os.path.join(download_dir, exchange)
                )
                print(f"✓ {exchange.upper()} download completed with symbol {symbol}!")
                success += 1
                break
            except Exception as e:
                print(f"✗ Error downloading {exchange} ({symbol}): {e}")
        if success == 0:
            print(f"⚠ No successful downloads for {exchange}. Check symbol mapping or API access.")

    # Verify downloads
    subdirs = [d for d in os.listdir(download_dir) if os.path.isdir(os.path.join(download_dir, d)) and d not in {"__pycache__"}]
    if subdirs:
        print(f"\n✓ Success: Downloaded data from {len(subdirs)} exchanges.")
    else:
        print("\n⚠ Warning: No files found. Check API key access and date validity.")


def compare_prices():
    """
    Compare minimum prices across exchanges for DOGE.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = script_dir

    print("\n--- Price Comparison Analysis (DOGE) ---")

    if not os.path.exists(download_dir):
        print("No data directory found. Run download_spot_trades() first.")
        return

    results = {}

    for exchange in EXCHANGES:
        exchange_dir = os.path.join(download_dir, exchange)
        if os.path.exists(exchange_dir):
            files = [f for f in os.listdir(exchange_dir) if f.endswith('.csv') or f.endswith('.csv.gz')]
            if files:
                try:
                    df = pd.read_csv(os.path.join(exchange_dir, files[0]))
                    min_price = df['price'].min() if 'price' in df.columns else None
                    max_price = df['price'].max() if 'price' in df.columns else None
                    results[exchange] = {
                        'min': min_price,
                        'max': max_price,
                        'records': len(df)
                    }
                    print(f"{exchange.upper()}: Min=${min_price:.8f} | Max=${max_price:.8f} | Records={len(df)}")
                except Exception as e:
                    print(f"Error reading {exchange} data: {e}")

    if 'binance' in results:
        binance_min = results['binance']['min']
        print(f"\n--- Price Differential vs Binance (Min: ${binance_min:.8f}) ---")
        for exchange in EXCHANGES:
            if exchange in results and exchange != 'binance':
                diff = results[exchange]['min'] - binance_min
                pct = (diff / binance_min) * 100
                print(f"{exchange.upper()}: ${diff:+.8f} ({pct:+.4f}%)")

if __name__ == "__main__":
    download_spot_trades()
    compare_prices()
