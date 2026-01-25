import os
import pandas as pd
import sys

# Handle console encoding on Windows for non-ASCII paths
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def get_price_data(coin_dir):
    """
    Extract min/max prices for Binance (baseline), Coinbase, and Gemini only.
    """
    results = {}
    exchanges_to_keep = {"binance", "coinbase", "gemini"}
    
    if not os.path.isdir(coin_dir):
        return results
    
    for exchange in os.listdir(coin_dir):
        exchange_path = os.path.join(coin_dir, exchange)
        if not os.path.isdir(exchange_path) or exchange in {"__pycache__"}:
            continue
        
        # Only keep Binance, Coinbase, and Gemini
        if exchange not in exchanges_to_keep:
            continue
        
        files = [f for f in os.listdir(exchange_path) if f.endswith('.csv') or f.endswith('.csv.gz')]
        if files:
            try:
                # Read in chunks for large files to avoid memory issues
                df = pd.read_csv(os.path.join(exchange_path, files[0]), usecols=['price'])
                if 'price' in df.columns and len(df) > 0:
                    min_price = df['price'].min()
                    max_price = df['price'].max()
                    results[exchange] = {
                        'min': min_price,
                        'max': max_price,
                        'records': len(df)
                    }
            except Exception as e:
                print(f"⚠ Error reading {exchange} data: {e}")
    
    return results

def compare_all_coins():
    """
    Compare Coinbase and Gemini against Binance baseline (concise output).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    spot_dir = script_dir

    # Original coins + liquidated coins from 2025-10-10 incident
    coins = ["BTC", "DOGE", "AAVE", "SOL", "POL", 
             "CRV", "WIF", "PEPE", "SKY", "ENA", "BB", "BONK", "WLD"]
    
    # For PEPE and BONK: spot markets use same units (no multiplier needed)
    # Only futures use 1000PEPE/1000BONK
    multiplier_coins = {}

    print("Binance baseline vs Coinbase / Gemini (2025-10-10)\n")

    for coin in coins:
        coin_path = os.path.join(spot_dir, coin)
        results = get_price_data(coin_path)

        if not results:
            print(f"{coin}: no data\n")
            continue

        if "binance" not in results:
            print(f"{coin}: binance missing, skip\n")
            continue

        binance_min = results["binance"]["min"]
        binance_rec = results["binance"].get("records", 0)

        # Choose display precision per coin
        if coin == "BTC":
            fmt = "{:.2f}"
        elif coin == "DOGE":
            fmt = "{:.8f}"
        else:
            fmt = "{:.6f}"

        print(f"{coin}:")
        print(f"  Binance min {fmt.format(binance_min)} ({binance_rec:,} records)")

        # Get multiplier for coins like PEPE/BONK
        multiplier = multiplier_coins.get(coin, 1)

        for ex in ["coinbase", "gemini"]:
            if ex in results:
                ex_min = results[ex]["min"]
                # Apply multiplier for comparison (Coinbase PEPE -> Binance 1000PEPE)
                adjusted_min = ex_min * multiplier
                diff = adjusted_min - binance_min
                pct = (diff / binance_min) * 100 if binance_min else 0
                if multiplier > 1:
                    print(f"  {ex.capitalize()} min {fmt.format(ex_min)} (x{multiplier}={fmt.format(adjusted_min)}) | vs Binance {pct:+.4f}%")
                else:
                    print(f"  {ex.capitalize()} min {fmt.format(ex_min)} | vs Binance {pct:+.4f}%")

        print("")

if __name__ == "__main__":
    compare_all_coins()
