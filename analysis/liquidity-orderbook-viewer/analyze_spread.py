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

def analyze_spread(filepath, sample_size=100000):
    """Analyze bid-ask spread for an exchange"""
    print(f"\nAnalyzing {filepath}...")
    
    # Read data
    df = pd.read_csv(filepath, nrows=sample_size)
    
    # Calculate spread for each row
    df['best_bid'] = df['bids[0].price']
    df['best_ask'] = df['asks[0].price']
    df['spread_absolute'] = df['best_ask'] - df['best_bid']
    df['spread_bps'] = (df['spread_absolute'] / df['best_bid']) * 10000  # basis points
    df['mid_price'] = (df['best_bid'] + df['best_ask']) / 2
    
    # Remove any invalid data
    df = df[df['spread_absolute'] >= 0]
    
    # Statistics
    mean_spread = df['spread_absolute'].mean()
    median_spread = df['spread_absolute'].median()
    min_spread = df['spread_absolute'].min()
    max_spread = df['spread_absolute'].max()
    std_spread = df['spread_absolute'].std()
    
    mean_spread_bps = df['spread_bps'].mean()
    median_spread_bps = df['spread_bps'].median()
    
    mean_bid = df['best_bid'].mean()
    mean_ask = df['best_ask'].mean()
    mean_mid = df['mid_price'].mean()
    
    # Spread distribution
    spread_percentiles = df['spread_absolute'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    
    # Count tight spreads (< $1, < $5, < $10)
    tight_1 = (df['spread_absolute'] < 1).sum()
    tight_5 = (df['spread_absolute'] < 5).sum()
    tight_10 = (df['spread_absolute'] < 10).sum()
    
    return {
        'total_rows': len(df),
        'mean_spread': mean_spread,
        'median_spread': median_spread,
        'min_spread': min_spread,
        'max_spread': max_spread,
        'std_spread': std_spread,
        'mean_spread_bps': mean_spread_bps,
        'median_spread_bps': median_spread_bps,
        'mean_bid': mean_bid,
        'mean_ask': mean_ask,
        'mean_mid': mean_mid,
        'percentiles': spread_percentiles,
        'tight_1_count': tight_1,
        'tight_5_count': tight_5,
        'tight_10_count': tight_10,
        'tight_1_pct': tight_1 / len(df) * 100,
        'tight_5_pct': tight_5 / len(df) * 100,
        'tight_10_pct': tight_10 / len(df) * 100,
    }

def main():
    print("=" * 100)
    print("BID-ASK SPREAD ANALYSIS - October 9, 2025")
    print("=" * 100)
    
    results = {}
    
    for name, filepath in EXCHANGES.items():
        try:
            result = analyze_spread(filepath)
            results[name] = result
            
            print(f"\n{name}:")
            print(f"  Sample size: {result['total_rows']:,} snapshots")
            print(f"  Average prices: Bid ${result['mean_bid']:,.2f} | Ask ${result['mean_ask']:,.2f} | Mid ${result['mean_mid']:,.2f}")
            print(f"  ")
            print(f"  Spread Statistics:")
            print(f"    Mean: ${result['mean_spread']:.2f} ({result['mean_spread_bps']:.2f} bps)")
            print(f"    Median: ${result['median_spread']:.2f} ({result['median_spread_bps']:.2f} bps)")
            print(f"    Min: ${result['min_spread']:.2f}")
            print(f"    Max: ${result['max_spread']:.2f}")
            print(f"    Std Dev: ${result['std_spread']:.2f}")
            print(f"  ")
            print(f"  Spread Distribution:")
            print(f"    25th percentile: ${result['percentiles'][0.25]:.2f}")
            print(f"    50th percentile: ${result['percentiles'][0.5]:.2f}")
            print(f"    75th percentile: ${result['percentiles'][0.75]:.2f}")
            print(f"    90th percentile: ${result['percentiles'][0.9]:.2f}")
            print(f"    95th percentile: ${result['percentiles'][0.95]:.2f}")
            print(f"    99th percentile: ${result['percentiles'][0.99]:.2f}")
            print(f"  ")
            print(f"  Tight Spreads:")
            print(f"    < $1: {result['tight_1_count']:,} ({result['tight_1_pct']:.1f}%)")
            print(f"    < $5: {result['tight_5_count']:,} ({result['tight_5_pct']:.1f}%)")
            print(f"    < $10: {result['tight_10_count']:,} ({result['tight_10_pct']:.1f}%)")
                
        except Exception as e:
            print(f"\n{name}: ❌ Error - {e}")
    
    # Summary comparison
    print("\n" + "=" * 100)
    print("SUMMARY - Spread Comparison")
    print("=" * 100)
    print(f"{'Exchange':<20} {'Mean Spread':<15} {'Median Spread':<15} {'Mean (bps)':<12} {'< $1 Spread':<15}")
    print("-" * 100)
    
    for name, result in results.items():
        print(f"{name:<20} ${result['mean_spread']:>13.2f}  ${result['median_spread']:>13.2f}  {result['mean_spread_bps']:>10.2f}  {result['tight_1_pct']:>13.1f}%")
    
    # Rankings
    print("\n" + "=" * 100)
    print("RANKINGS:")
    print("=" * 100)
    
    # Tightest spreads
    tightest = sorted(results.items(), key=lambda x: x[1]['mean_spread'])
    print("\n1. TIGHTEST SPREADS (Best for traders):")
    for i, (name, result) in enumerate(tightest[:3], 1):
        print(f"   {i}. {name}: ${result['mean_spread']:.2f} ({result['mean_spread_bps']:.2f} bps)")
    
    # Widest spreads
    widest = sorted(results.items(), key=lambda x: x[1]['mean_spread'], reverse=True)
    print("\n2. WIDEST SPREADS:")
    for i, (name, result) in enumerate(widest[:3], 1):
        print(f"   {i}. {name}: ${result['mean_spread']:.2f} ({result['mean_spread_bps']:.2f} bps)")
    
    # Most consistent (lowest std dev)
    most_consistent = sorted(results.items(), key=lambda x: x[1]['std_spread'])
    print("\n3. MOST CONSISTENT SPREADS (Lowest volatility):")
    for i, (name, result) in enumerate(most_consistent[:3], 1):
        print(f"   {i}. {name}: Std Dev ${result['std_spread']:.2f}")
    
    # Highest percentage of tight spreads
    tightest_pct = sorted(results.items(), key=lambda x: x[1]['tight_1_pct'], reverse=True)
    print("\n4. HIGHEST % OF SUB-$1 SPREADS:")
    for i, (name, result) in enumerate(tightest_pct[:3], 1):
        print(f"   {i}. {name}: {result['tight_1_pct']:.1f}% of snapshots")
    
    print("\n" + "=" * 100)
    print("INTERPRETATION:")
    print("=" * 100)
    print("• Spread = Best Ask Price - Best Bid Price")
    print("• Tighter spreads = Lower trading costs")
    print("• 1 basis point (bp) = 0.01%")
    print("• For BTC at ~$123,000, 1 bp ≈ $12.30")
    print("=" * 100)

if __name__ == "__main__":
    main()
