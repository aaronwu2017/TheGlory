import pandas as pd
import numpy as np

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

def analyze_depth_range(filepath, sample_size=100000):
    """Analyze the range from worst bid to worst ask across 25 levels"""
    print(f"\nAnalyzing {filepath}...")
    
    # Read data
    df = pd.read_csv(filepath, nrows=sample_size)
    
    # Get best and worst prices
    df['best_bid'] = df['bids[0].price']
    df['best_ask'] = df['asks[0].price']
    df['worst_bid'] = df['bids[24].price']
    df['worst_ask'] = df['asks[24].price']
    
    # Calculate ranges
    df['full_range'] = df['worst_ask'] - df['worst_bid']
    df['bid_depth'] = df['best_bid'] - df['worst_bid']  # How far bids go down
    df['ask_depth'] = df['worst_ask'] - df['best_ask']  # How far asks go up
    df['mid_price'] = (df['best_bid'] + df['best_ask']) / 2
    
    # Calculate as percentage of mid price
    df['full_range_pct'] = (df['full_range'] / df['mid_price']) * 100
    df['bid_depth_pct'] = (df['bid_depth'] / df['mid_price']) * 100
    df['ask_depth_pct'] = (df['ask_depth'] / df['mid_price']) * 100
    
    # Remove invalid data
    df = df.dropna(subset=['worst_bid', 'worst_ask'])
    
    # Statistics
    return {
        'total_rows': len(df),
        'avg_mid_price': df['mid_price'].mean(),
        'avg_best_bid': df['best_bid'].mean(),
        'avg_best_ask': df['best_ask'].mean(),
        'avg_worst_bid': df['worst_bid'].mean(),
        'avg_worst_ask': df['worst_ask'].mean(),
        'avg_full_range': df['full_range'].mean(),
        'median_full_range': df['full_range'].median(),
        'min_full_range': df['full_range'].min(),
        'max_full_range': df['full_range'].max(),
        'avg_full_range_pct': df['full_range_pct'].mean(),
        'avg_bid_depth': df['bid_depth'].mean(),
        'avg_ask_depth': df['ask_depth'].mean(),
        'avg_bid_depth_pct': df['bid_depth_pct'].mean(),
        'avg_ask_depth_pct': df['ask_depth_pct'].mean(),
    }

def main():
    print("=" * 100)
    print("ORDERBOOK DEPTH RANGE ANALYSIS - October 9, 2025")
    print("Range from Worst Bid (bids[24]) to Worst Ask (asks[24])")
    print("=" * 100)
    
    results = {}
    
    for name, filepath in EXCHANGES.items():
        try:
            result = analyze_depth_range(filepath)
            results[name] = result
            
            print(f"\n{name}:")
            print(f"  Sample size: {result['total_rows']:,} snapshots")
            print(f"  Average mid price: ${result['avg_mid_price']:,.2f}")
            print(f"  ")
            print(f"  Price Levels:")
            print(f"    Best Bid:  ${result['avg_best_bid']:,.2f}")
            print(f"    Best Ask:  ${result['avg_best_ask']:,.2f}")
            print(f"    Worst Bid: ${result['avg_worst_bid']:,.2f}")
            print(f"    Worst Ask: ${result['avg_worst_ask']:,.2f}")
            print(f"  ")
            print(f"  Depth Range:")
            print(f"    Full Range (worst bid → worst ask): ${result['avg_full_range']:,.2f} ({result['avg_full_range_pct']:.3f}%)")
            print(f"    Bid Depth (best → worst bid):       ${result['avg_bid_depth']:,.2f} ({result['avg_bid_depth_pct']:.3f}%)")
            print(f"    Ask Depth (best → worst ask):       ${result['avg_ask_depth']:,.2f} ({result['avg_ask_depth_pct']:.3f}%)")
            print(f"  ")
            print(f"  Range Statistics:")
            print(f"    Mean:   ${result['avg_full_range']:,.2f}")
            print(f"    Median: ${result['median_full_range']:,.2f}")
            print(f"    Min:    ${result['min_full_range']:,.2f}")
            print(f"    Max:    ${result['max_full_range']:,.2f}")
                
        except Exception as e:
            print(f"\n{name}: ❌ Error - {e}")
    
    # Summary comparison
    print("\n" + "=" * 100)
    print("SUMMARY - Orderbook Depth Comparison")
    print("=" * 100)
    print(f"{'Exchange':<20} {'Avg Mid Price':<15} {'Full Range':<15} {'Range %':<12} {'Bid Depth':<15} {'Ask Depth':<15}")
    print("-" * 100)
    
    for name, result in results.items():
        print(f"{name:<20} ${result['avg_mid_price']:>13,.2f}  ${result['avg_full_range']:>13,.2f}  {result['avg_full_range_pct']:>10.3f}%  ${result['avg_bid_depth']:>13,.2f}  ${result['avg_ask_depth']:>13,.2f}")
    
    # Check if ranges are similar across exchanges
    print("\n" + "=" * 100)
    print("CROSS-EXCHANGE COMPARISON:")
    print("=" * 100)
    
    # Compare mid prices
    mid_prices = [r['avg_mid_price'] for r in results.values()]
    mid_price_range = max(mid_prices) - min(mid_prices)
    mid_price_pct_diff = (mid_price_range / np.mean(mid_prices)) * 100
    
    print(f"\n1. MID PRICE CONSISTENCY:")
    print(f"   Range: ${min(mid_prices):,.2f} to ${max(mid_prices):,.2f}")
    print(f"   Difference: ${mid_price_range:,.2f} ({mid_price_pct_diff:.3f}%)")
    if mid_price_pct_diff < 0.5:
        print(f"   ✓ Prices are VERY SIMILAR across exchanges")
    elif mid_price_pct_diff < 1.0:
        print(f"   ⚠ Prices have MINOR differences across exchanges")
    else:
        print(f"   ✗ Prices have SIGNIFICANT differences across exchanges")
    
    # Compare depth ranges
    ranges = [r['avg_full_range'] for r in results.values()]
    range_pcts = [r['avg_full_range_pct'] for r in results.values()]
    
    print(f"\n2. ORDERBOOK DEPTH RANGE:")
    print(f"   Narrowest: ${min(ranges):,.2f} ({min(range_pcts):.3f}%)")
    print(f"   Widest:    ${max(ranges):,.2f} ({max(range_pcts):.3f}%)")
    print(f"   Ratio:     {max(ranges)/min(ranges):.2f}x difference")
    
    # Rankings
    narrowest = sorted(results.items(), key=lambda x: x[1]['avg_full_range'])
    widest = sorted(results.items(), key=lambda x: x[1]['avg_full_range'], reverse=True)
    
    print(f"\n3. NARROWEST DEPTH (25 levels):")
    for i, (name, result) in enumerate(narrowest[:3], 1):
        print(f"   {i}. {name}: ${result['avg_full_range']:,.2f} ({result['avg_full_range_pct']:.3f}%)")
    
    print(f"\n4. WIDEST DEPTH (25 levels):")
    for i, (name, result) in enumerate(widest[:3], 1):
        print(f"   {i}. {name}: ${result['avg_full_range']:,.2f} ({result['avg_full_range_pct']:.3f}%)")
    
    print("\n" + "=" * 100)
    print("INTERPRETATION:")
    print("=" * 100)
    print("• Full Range = Distance from worst bid (bids[24]) to worst ask (asks[24])")
    print("• Narrower range = More concentrated liquidity")
    print("• Wider range = Liquidity spread over larger price range")
    print("• Similar mid prices = Efficient arbitrage across exchanges")
    print("=" * 100)

if __name__ == "__main__":
    main()
