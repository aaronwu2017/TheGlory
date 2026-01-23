import pandas as pd
import numpy as np
from datetime import datetime

# Define exchanges to analyze
EXCHANGES = {
    "Binance USDT": "datasets/Oct 9/binance-futures_book_snapshot_25_2025-10-09_BTCUSDT.csv",
    "OKX USDT": "datasets/Oct 9/okex-swap_book_snapshot_25_2025-10-09_BTC-USDT-SWAP.csv",
    "Bybit": "datasets/Oct 9/bybit_book_snapshot_25_2025-10-09_BTCPERP.csv",
    "Huobi": "datasets/Oct 9/huobi-dm-linear-swap_book_snapshot_25_2025-10-09_BTC-USDT.csv",
    "KuCoin USDC": "datasets/Oct 9/kucoin-futures_book_snapshot_25_2025-10-09_XBTUSDCM.csv",
    "Hyperliquid": "datasets/Oct 9/hyperliquid_book_snapshot_25_2025-10-09_BTC.csv",
    "Bitget": "datasets/Oct 9/bitget-futures_book_snapshot_25_2025-10-09_BTCUSDT.csv",
    "Coinbase": "datasets/Oct 9/coinbase-international_book_snapshot_25_2025-10-09_BTC-PERP.csv",
}

def timestamp_to_utc(timestamp_us):
    """Convert microsecond timestamp to UTC datetime"""
    return datetime.utcfromtimestamp(timestamp_us / 1_000_000)

def analyze_timestamps(filepath, sample_size=100000):
    """Analyze timestamp intervals for an exchange"""
    print(f"\nReading {filepath}...")
    
    # Read first chunk to analyze
    df = pd.read_csv(filepath, nrows=sample_size)
    
    # Calculate intervals in milliseconds
    df['timestamp_diff'] = df['timestamp'].diff()
    df['interval_ms'] = df['timestamp_diff'] / 1000  # Convert microseconds to milliseconds
    
    # Remove first row (NaN) and outliers
    intervals = df['interval_ms'].dropna()
    intervals = intervals[intervals > 0]  # Remove negative intervals if any
    
    # Statistics
    mean_interval = intervals.mean()
    median_interval = intervals.median()
    min_interval = intervals.min()
    max_interval = intervals.max()
    std_interval = intervals.std()
    
    # Frequency (snapshots per second)
    frequency = 1000 / mean_interval if mean_interval > 0 else 0
    
    # Check if timestamps are synchronized (same across exchanges)
    first_timestamp = df['timestamp'].iloc[0]
    last_timestamp = df['timestamp'].iloc[-1]
    first_time = timestamp_to_utc(first_timestamp)
    last_time = timestamp_to_utc(last_timestamp)
    
    # Count unique intervals (to see if it's fixed or variable)
    unique_intervals = intervals.round(1).value_counts().head(5)
    
    return {
        'total_rows': len(df),
        'mean_interval_ms': mean_interval,
        'median_interval_ms': median_interval,
        'min_interval_ms': min_interval,
        'max_interval_ms': max_interval,
        'std_interval_ms': std_interval,
        'frequency_per_sec': frequency,
        'first_timestamp': first_timestamp,
        'last_timestamp': last_timestamp,
        'first_time': first_time,
        'last_time': last_time,
        'unique_intervals': unique_intervals
    }

def main():
    print("=" * 100)
    print("TIMESTAMP INTERVAL ANALYSIS - October 9, 2025")
    print("=" * 100)
    
    results = {}
    
    for name, filepath in EXCHANGES.items():
        try:
            result = analyze_timestamps(filepath)
            results[name] = result
            
            print(f"\n{name}:")
            print(f"  Sample size: {result['total_rows']:,} rows")
            print(f"  First timestamp: {result['first_time']} UTC ({result['first_timestamp']})")
            print(f"  Last timestamp: {result['last_time']} UTC ({result['last_timestamp']})")
            print(f"  Mean interval: {result['mean_interval_ms']:.2f} ms")
            print(f"  Median interval: {result['median_interval_ms']:.2f} ms")
            print(f"  Min interval: {result['min_interval_ms']:.2f} ms")
            print(f"  Max interval: {result['max_interval_ms']:.2f} ms")
            print(f"  Std deviation: {result['std_interval_ms']:.2f} ms")
            print(f"  Frequency: ~{result['frequency_per_sec']:.2f} snapshots/second")
            print(f"  Top 5 most common intervals (ms):")
            for interval, count in result['unique_intervals'].items():
                print(f"    {interval:.1f} ms: {count:,} times ({count/result['total_rows']*100:.1f}%)")
                
        except Exception as e:
            print(f"\n{name}: ❌ Error - {e}")
    
    # Summary comparison
    print("\n" + "=" * 100)
    print("SUMMARY - Timestamp Characteristics")
    print("=" * 100)
    print(f"{'Exchange':<20} {'Mean Interval':<15} {'Frequency':<15} {'First Timestamp':<25} {'Synchronized?':<15}")
    print("-" * 100)
    
    # Check if timestamps are synchronized across exchanges
    first_timestamps = [r['first_timestamp'] for r in results.values()]
    timestamps_synced = len(set(first_timestamps)) == 1
    
    for name, result in results.items():
        synced_str = "✓ Yes" if timestamps_synced else "✗ No"
        print(f"{name:<20} {result['mean_interval_ms']:>13.2f} ms  {result['frequency_per_sec']:>13.2f}/s  {result['first_time'].strftime('%Y-%m-%d %H:%M:%S'):<25} {synced_str:<15}")
    
    print("\n" + "=" * 100)
    print("KEY FINDINGS:")
    print("=" * 100)
    
    # Find fastest and slowest
    fastest = min(results.items(), key=lambda x: x[1]['mean_interval_ms'])
    slowest = max(results.items(), key=lambda x: x[1]['mean_interval_ms'])
    
    print(f"1. FASTEST UPDATE RATE:")
    print(f"   {fastest[0]}: {fastest[1]['frequency_per_sec']:.2f} snapshots/second ({fastest[1]['mean_interval_ms']:.2f} ms interval)")
    
    print(f"\n2. SLOWEST UPDATE RATE:")
    print(f"   {slowest[0]}: {slowest[1]['frequency_per_sec']:.2f} snapshots/second ({slowest[1]['mean_interval_ms']:.2f} ms interval)")
    
    print(f"\n3. TIMESTAMP SYNCHRONIZATION:")
    if timestamps_synced:
        print(f"   ✓ All exchanges start at the same timestamp")
        print(f"   First timestamp: {list(results.values())[0]['first_time']} UTC")
    else:
        print(f"   ✗ Exchanges have different starting timestamps")
        for name, result in results.items():
            print(f"   {name}: {result['first_time']} UTC")
    
    print(f"\n4. UPDATE PATTERN:")
    # Check if intervals are fixed or variable
    for name, result in results.items():
        top_interval_pct = result['unique_intervals'].iloc[0] / result['total_rows'] * 100
        if top_interval_pct > 80:
            print(f"   {name}: FIXED interval (~{result['median_interval_ms']:.0f} ms)")
        else:
            print(f"   {name}: VARIABLE intervals (mean: {result['mean_interval_ms']:.0f} ms)")

if __name__ == "__main__":
    main()
