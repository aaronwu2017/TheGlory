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

# Exchange-specific BTC/USD symbol mapping
SYMBOL_MAP = {
    "binance": ["BTCUSDT"],
    "coinbase": ["BTC-USD"],
    "gemini": ["BTCUSD"],
}

def download_spot_trades():
    """
    Downloads spot trading data from major compliant exchanges:
    - Binance
    - OKEx
    - Bitfinex
    - Coinbase
    - Kraken
    - Gemini
    - Bybit Spot
    - KuCoin
    - Gate.io
    - Bitget
    
    Compare bid/ask/mark prices across exchanges.
    """
    # API Key from options folder
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"
    
    # Ensure the download directory exists (store alongside this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = script_dir
    os.makedirs(download_dir, exist_ok=True)

    print(f"Starting spot trade data downloads...")
    print(f"Saving to: {download_dir}")
    print(f"Target exchanges: {', '.join(EXCHANGES)}")
    print(f"Using API Key: {api_key[:5]}... (Check if this key has access to the requested dates)")

    for exchange in EXCHANGES:
        exchange_symbols = SYMBOL_MAP.get(exchange, ["BTCUSDT"])
        success = 0
        print(f"\n--- Downloading {exchange.upper()} spot trades ---")
        for symbol in exchange_symbols:
            try:
                datasets.download(
                    exchange=exchange,
                    
                    # 'trades' data type includes:
                    # - price (last traded price)
                    # - side (buy/sell)
                    # - amount
                    # - timestamp
                    data_types=["trades"],
                    
                    # Date range: 2025-10-10 (incident date)
                    from_date="2025-10-10",
                    to_date="2025-10-11",
                    
                    symbols=[symbol],
                    
                    api_key=api_key,
                    download_dir=os.path.join(download_dir, exchange)
                )
                print(f"✓ {exchange.upper()} download completed with symbol {symbol}!")
                success += 1
                # Stop after first success per exchange
                break
            except Exception as e:
                print(f"✗ Error downloading {exchange} ({symbol}): {str(e)}")
        if success == 0:
            print(f"⚠ No successful downloads for {exchange}. Check symbol mapping or API access.")
    
    # Verify downloads
    if os.path.exists(download_dir) and os.listdir(download_dir):
        print(f"\n✓ Success: Downloaded data from {len(os.listdir(download_dir))} exchanges.")
    else:
        print("\n⚠ Warning: No files found. Check API key access and date validity.")

def compare_prices():
    """
    Compare minimum prices across exchanges.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = script_dir
    
    print("\n--- Price Comparison Analysis ---")
    
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
                    print(f"{exchange.upper()}: Min=${min_price:.2f} | Max=${max_price:.2f} | Records={len(df)}")
                except Exception as e:
                    print(f"Error reading {exchange} data: {e}")
    
    # Compare with Binance baseline
    if 'binance' in results:
        binance_min = results['binance']['min']
        print(f"\n--- Price Differential vs Binance (Min: ${binance_min:.2f}) ---")
        for exchange in ["coinbase", "kraken"]:
            if exchange in results:
                diff = results[exchange]['min'] - binance_min
                pct = (diff / binance_min) * 100
                print(f"{exchange.upper()}: ${diff:+.2f} ({pct:+.2f}%)")

if __name__ == "__main__":
    download_spot_trades()
    compare_prices()
