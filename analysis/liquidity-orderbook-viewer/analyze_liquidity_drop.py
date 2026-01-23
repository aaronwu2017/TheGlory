import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define exchanges to analyze
EXCHANGES = {
    "Binance USDT": {
        "baseline": "datasets/Oct 9/binance-futures_book_snapshot_25_2025-10-09_BTCUSDT.csv",
        "drop": "datasets/Oct 10/binance-futures_book_snapshot_25_2025-10-10_BTCUSDT.csv"
    },
    "OKX USDT": {
        "baseline": "datasets/Oct 9/okex-swap_book_snapshot_25_2025-10-09_BTC-USDT-SWAP.csv",
        "drop": "datasets/Oct 10/okex-swap_book_snapshot_25_2025-10-10_BTC-USDT-SWAP.csv"
    },
    "Bybit": {
        "baseline": "datasets/Oct 9/bybit_book_snapshot_25_2025-10-09_BTCPERP.csv",
        "drop": "datasets/Oct 10/bybit_book_snapshot_25_2025-10-10_BTCPERP.csv"
    },
    "Huobi": {
        "baseline": "datasets/Oct 9/huobi-dm-linear-swap_book_snapshot_25_2025-10-09_BTC-USDT.csv",
        "drop": "datasets/Oct 10/huobi-dm-linear-swap_book_snapshot_25_2025-10-10_BTC-USDT.csv"
    },
    "KuCoin USDC": {
        "baseline": "datasets/Oct 9/kucoin-futures_book_snapshot_25_2025-10-09_XBTUSDCM.csv",
        "drop": "datasets/Oct 10/kucoin-futures_book_snapshot_25_2025-10-10_XBTUSDCM.csv"
    },
    "Hyperliquid": {
        "baseline": "datasets/Oct 9/hyperliquid_book_snapshot_25_2025-10-09_BTC.csv",
        "drop": "datasets/Oct 10/hyperliquid_book_snapshot_25_2025-10-10_BTC.csv"
    },
    "Bitget": {
        "baseline": "datasets/Oct 9/bitget-futures_book_snapshot_25_2025-10-09_BTCUSDT.csv",
        "drop": "datasets/Oct 10/bitget-futures_book_snapshot_25_2025-10-10_BTCUSDT.csv"
    },
    "Coinbase": {
        "baseline": "datasets/Oct 9/coinbase-international_book_snapshot_25_2025-10-09_BTC-PERP.csv",
        "drop": "datasets/Oct 10/coinbase-international_book_snapshot_25_2025-10-10_BTC-PERP.csv"
    },
}

def timestamp_to_utc(timestamp_us):
    """Convert microsecond timestamp to UTC datetime"""
    return datetime.utcfromtimestamp(timestamp_us / 1_000_000)

def calculate_liquidity(df_chunk):
    """Calculate total bid and ask liquidity for a chunk of data"""
    bid_liquidity = 0
    ask_liquidity = 0
    
    for i in range(25):
        bid_col_price = f'bids[{i}].price'
        bid_col_amount = f'bids[{i}].amount'
        ask_col_price = f'asks[{i}].price'
        ask_col_amount = f'asks[{i}].amount'
        
        if bid_col_price in df_chunk.columns and bid_col_amount in df_chunk.columns:
            bid_liquidity += (df_chunk[bid_col_price] * df_chunk[bid_col_amount]).sum()
        if ask_col_price in df_chunk.columns and ask_col_amount in df_chunk.columns:
            ask_liquidity += (df_chunk[ask_col_price] * df_chunk[ask_col_amount]).sum()
    
    return bid_liquidity, ask_liquidity

def analyze_exchange(name, baseline_filepath, drop_filepath, drop_start, drop_end):
    """Analyze liquidity changes for a single exchange"""
    print(f"\nAnalyzing {name}...")
    
    # Convert drop times to microseconds
    drop_start_ts = int(drop_start.timestamp() * 1_000_000)
    drop_end_ts = int(drop_end.timestamp() * 1_000_000)
    
    # Read baseline data (entire Oct 9) - sample every Nth row for efficiency
    print(f"  Loading Oct 9 baseline data...")
    chunk_size = 100000
    baseline_data = []
    
    for chunk in pd.read_csv(baseline_filepath, chunksize=chunk_size):
        # Sample every 10th row to reduce memory usage
        sampled = chunk.iloc[::10]
        baseline_data.append(sampled)
    
    df_baseline = pd.concat(baseline_data)
    print(f"  Baseline: {len(df_baseline):,} data points (sampled from Oct 9)")
    
    # Read drop period data from Oct 10
    print(f"  Loading Oct 10 drop period data...")
    drop_data = []
    
    for chunk in pd.read_csv(drop_filepath, chunksize=chunk_size):
        # Filter drop period data
        drop_chunk = chunk[(chunk['timestamp'] >= drop_start_ts) & 
                          (chunk['timestamp'] <= drop_end_ts)]
        if len(drop_chunk) > 0:
            drop_data.append(drop_chunk)
        
        # Stop if we've passed the time window
        if chunk['timestamp'].min() > drop_end_ts:
            break
    
    if not drop_data:
        print(f"  ⚠️  No data found in drop period")
        return None
    
    df_drop = pd.concat(drop_data)
    print(f"  Drop period: {len(df_drop):,} data points")
    
    # Sample drop data for computation (baseline already sampled during load)
    sample_rate_drop = max(1, len(df_drop) // 100)
    df_drop_sample = df_drop.iloc[::sample_rate_drop]
    
    # Calculate average liquidity
    bid_liq_baseline, ask_liq_baseline = calculate_liquidity(df_baseline)
    bid_liq_drop, ask_liq_drop = calculate_liquidity(df_drop_sample)
    
    # Calculate averages
    bid_avg_baseline = bid_liq_baseline / len(df_baseline)
    ask_avg_baseline = ask_liq_baseline / len(df_baseline)
    bid_avg_drop = bid_liq_drop / len(df_drop_sample)
    ask_avg_drop = ask_liq_drop / len(df_drop_sample)
    
    total_baseline = bid_avg_baseline + ask_avg_baseline
    total_drop = bid_avg_drop + ask_avg_drop
    
    # Calculate changes
    bid_change_pct = ((bid_avg_drop - bid_avg_baseline) / bid_avg_baseline * 100) if bid_avg_baseline > 0 else 0
    ask_change_pct = ((ask_avg_drop - ask_avg_baseline) / ask_avg_baseline * 100) if ask_avg_baseline > 0 else 0
    total_change_pct = ((total_drop - total_baseline) / total_baseline * 100) if total_baseline > 0 else 0
    
    print(f"  Data points: {len(df_baseline)} baseline, {len(df_drop)} during drop")
    print(f"  Bid liquidity: ${bid_avg_baseline:,.0f} → ${bid_avg_drop:,.0f} ({bid_change_pct:+.2f}%)")
    print(f"  Ask liquidity: ${ask_avg_baseline:,.0f} → ${ask_avg_drop:,.0f} ({ask_change_pct:+.2f}%)")
    print(f"  Total liquidity: ${total_baseline:,.0f} → ${total_drop:,.0f} ({total_change_pct:+.2f}%)")
    
    return {
        'exchange': name,
        'bid_baseline': bid_avg_baseline,
        'bid_drop': bid_avg_drop,
        'ask_baseline': ask_avg_baseline,
        'ask_drop': ask_avg_drop,
        'total_baseline': total_baseline,
        'total_drop': total_drop,
        'bid_change_pct': bid_change_pct,
        'ask_change_pct': ask_change_pct,
        'total_change_pct': total_change_pct,
        'data_points_baseline': len(df_baseline),
        'data_points_drop': len(df_drop)
    }

def main():
    # Baseline: Full day Oct 9, 2025 (average liquidity)
    # Drop period: Oct 10, 2025 8:50-9:20 UTC (during the drop)
    drop_start = datetime(2025, 10, 10, 8, 50, 0)
    drop_end = datetime(2025, 10, 10, 9, 20, 0)
    
    print("=" * 80)
    print(f"LIQUIDITY DROP ANALYSIS")
    print(f"Baseline: October 9, 2025 (full day average)")
    print(f"Drop Period: October 10, 2025 {drop_start.strftime('%H:%M')} - {drop_end.strftime('%H:%M')} UTC")
    print("=" * 80)
    
    results = []
    
    for name, files in EXCHANGES.items():
        try:
            result = analyze_exchange(name, files["baseline"], files["drop"], drop_start, drop_end)
            if result:
                results.append(result)
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Sort by total liquidity change (most negative first)
    results.sort(key=lambda x: x['total_change_pct'])
    
    print("\n" + "=" * 80)
    print("SUMMARY - Exchanges Ranked by Liquidity Drop")
    print("=" * 80)
    print(f"{'Exchange':<20} {'Total Change':<15} {'Bid Change':<15} {'Ask Change':<15}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['exchange']:<20} {r['total_change_pct']:>+13.2f}%  {r['bid_change_pct']:>+13.2f}%  {r['ask_change_pct']:>+13.2f}%")
    
    print("\n" + "=" * 80)
    print("BIGGEST LIQUIDITY DROP:")
    if results:
        worst = results[0]
        print(f"  🔴 {worst['exchange']}")
        print(f"     Total liquidity dropped by {abs(worst['total_change_pct']):.2f}%")
        print(f"     From ${worst['total_baseline']:,.0f} to ${worst['total_drop']:,.0f}")
        print(f"     Bid: {worst['bid_change_pct']:+.2f}% | Ask: {worst['ask_change_pct']:+.2f}%")
    print("=" * 80)

if __name__ == "__main__":
    main()
