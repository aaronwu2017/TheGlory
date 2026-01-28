"""
Download Binance Coin-Margined Futures (COIN-M) data for price comparison.
Coin-margined contracts are settled in the underlying cryptocurrency (e.g., BTCUSD_PERP).
"""
from tardis_dev import datasets
import logging
import os
import pandas as pd
import sys

# Handle console encoding on Windows for non-ASCII paths
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Binance Coin-Margined (COIN-M) symbols
# Format: {COIN}USD_PERP for perpetual contracts
COIN_M_SYMBOLS = [
    "BTCUSD_PERP",    # Bitcoin
    "ETHUSD_PERP",    # Ethereum  
    "SOLUSD_PERP",    # Solana
    "DOGEUSD_PERP",   # Dogecoin
    "XRPUSD_PERP",    # XRP
    "BNBUSD_PERP",    # BNB
    "ADAUSD_PERP",    # Cardano
    "DOTUSD_PERP",    # Polkadot
    "LINKUSD_PERP",   # Chainlink
    "LTCUSD_PERP",    # Litecoin
    "BCHUSD_PERP",    # Bitcoin Cash
    "FILUSD_PERP",    # Filecoin
    "UNIUSD_PERP",    # Uniswap
    "ATOMUSD_PERP",   # Cosmos (ATOM)
    "AVAXUSD_PERP",   # Avalanche
    "TRXUSD_PERP",    # Tron
    "XLMUSD_PERP",    # Stellar
    "EOSUSD_PERP",    # EOS
    "AAVEUSD_PERP",   # Aave
    "MATICUSD_PERP",  # Polygon (Old)
    "POLUSD_PERP",    # Polygon (New)
    "MKRUSD_PERP",    # Maker (Old)
    "SKYUSD_PERP",    # Sky (New)
    "PEPEUSD_PERP",   # Pepe
    "BONKUSD_PERP",   # Bonk
    "ENAUSD_PERP",    # Ethena
    "CRVUSD_PERP",    # Curve
    "WLDUSD_PERP",    # Worldcoin
    "WIFUSD_PERP",    # dogwifhat
]

# Target coins from C-7 + ATOM
TARGET_COINS = ["BTC", "DOGE", "AAVE", "SOL", "POL", "CRV", "WIF", "PEPE", "SKY", "ENA", "BONK", "WLD", "ATOM"]

def download_coin_margined():
    """
    Downloads Binance Coin-Margined Futures data.
    Exchange name in Tardis: binance-delivery (for coin-margined futures)
    """
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(script_dir, "coin_margined")
    os.makedirs(download_dir, exist_ok=True)

    print(f"Starting Binance Coin-Margined Futures downloads...")
    print(f"Saving to: {download_dir}")
    print(f"Target symbols: {len(COIN_M_SYMBOLS)} contracts")

    successful = []
    failed = []
    
    for symbol in COIN_M_SYMBOLS:
        try:
            print(f"\n--- Downloading {symbol} ---")
            datasets.download(
                exchange="binance-delivery",  # Binance COIN-M futures
                data_types=["trades"],
                from_date="2025-10-10",
                to_date="2025-10-11",
                symbols=[symbol],
                api_key=api_key,
                download_dir=download_dir
            )
            print(f"✓ {symbol} download completed!")
            successful.append(symbol)
        except Exception as e:
            print(f"✗ Error downloading {symbol}: {str(e)}")
            failed.append(symbol)
    
    print(f"\n=== DOWNLOAD SUMMARY ===")
    print(f"Successful: {len(successful)} - {successful}")
    print(f"Failed: {len(failed)} - {failed}")
    
    return download_dir

def analyze_min_prices(download_dir=None):
    """
    Analyze minimum prices from downloaded Coin-M data.
    """
    if download_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(script_dir, "coin_margined")
    
    print("\n=== COIN-MARGINED MIN PRICE ANALYSIS ===\n")
    
    results = {}
    
    # Find all CSV files
    for file in os.listdir(download_dir):
        if file.endswith('.csv') or file.endswith('.csv.gz'):
            filepath = os.path.join(download_dir, file)
            try:
                df = pd.read_csv(filepath)
                if 'price' in df.columns:
                    min_price = df['price'].min()
                    max_price = df['price'].max()
                    
                    # Extract symbol from filename
                    # Format: binance-delivery_trades_2025-10-10_SYMBOL.csv.gz
                    # OR: binance-delivery_trades_2025-10-10_SYMBOL.csv
                    # We can remove the prefix and suffix
                    symbol = file
                    for prefix in ["binance-delivery_trades_2025-10-10_", "binance-delivery_trades_"]:
                        symbol = symbol.replace(prefix, "")
                    
                    symbol = symbol.replace(".csv.gz", "").replace(".csv", "")
                    
                    results[symbol] = {
                        'min': min_price,
                        'max': max_price,
                        'records': len(df),
                        'drop_pct': ((max_price - min_price) / max_price) * 100
                    }
                    print(f"{symbol}: Min=${min_price:.6f} | Max=${max_price:.2f} | Drop={results[symbol]['drop_pct']:.1f}%")
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    return results

if __name__ == "__main__":
    download_dir = download_coin_margined()
    analyze_min_prices(download_dir)
