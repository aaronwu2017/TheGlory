import pandas as pd
import numpy as np
from datetime import datetime

# Binance Oct 10 data
FILEPATH = "datasets/Oct 10/binance-futures_book_snapshot_25_2025-10-10_BTCUSDT.csv"

# Time range: 8:34 PM to 10:00 PM UTC (20:34 to 22:00)
START_TIME = datetime(2025, 10, 10, 20, 34, 0)
END_TIME = datetime(2025, 10, 10, 22, 0, 0)

# Liquidity ranges to analyze
RANGES = [
    (0, 10000, "Under $10K"),
    (10000, 20000, "$10K-$20K"),
    (20000, 50000, "$20K-$50K"),
    (50000, 100000, "$50K-$100K"),
    (100000, 500000, "$100K-$500K"),
    (500000, 1000000, "$500K-$1M"),
    (1000000, float('inf'), "Over $1M")
]

def calculate_bid_liquidity(row):
    """Calculate total bid liquidity for a single row"""
    bid_liquidity = 0
    for i in range(25):
        bid_price_col = f'bids[{i}].price'
        bid_amount_col = f'bids[{i}].amount'
        
        if bid_price_col in row.index and bid_amount_col in row.index:
            if pd.notna(row[bid_price_col]) and pd.notna(row[bid_amount_col]):
                bid_liquidity += row[bid_price_col] * row[bid_amount_col]
    
    return bid_liquidity

def main():
    print("=" * 80)
    print(f"BINANCE BID LIQUIDITY DISTRIBUTION ANALYSIS")
    print(f"Time Range: {START_TIME.strftime('%Y-%m-%d %H:%M')} - {END_TIME.strftime('%H:%M')} UTC")
    print("=" * 80)
    
    # Convert to microseconds - use actual date from data (2025-10-10)
    start_ts = 1760129640000000  # 2025-10-10 20:34:00 UTC
    end_ts = 1760135200000000    # 2025-10-10 22:00:00 UTC
    
    print(f"Start timestamp: {start_ts} ({datetime.utcfromtimestamp(start_ts / 1_000_000)})")
    print(f"End timestamp: {end_ts} ({datetime.utcfromtimestamp(end_ts / 1_000_000)})")
    
    print(f"\nLoading data from {START_TIME.strftime('%H:%M')} to {END_TIME.strftime('%H:%M')} UTC...")
    
    chunk_size = 100000
    filtered_data = []
    
    for chunk in pd.read_csv(FILEPATH, chunksize=chunk_size):
        # Filter by time range
        time_filtered = chunk[(chunk['timestamp'] >= start_ts) & 
                             (chunk['timestamp'] <= end_ts)]
        if len(time_filtered) > 0:
            filtered_data.append(time_filtered)
        
        # Stop if we've passed the time window
        if chunk['timestamp'].min() > end_ts:
            break
    
    if not filtered_data:
        print("No data found in specified time range!")
        return
    
    df = pd.concat(filtered_data)
    print(f"Found {len(df):,} snapshots in time range")
    
    # Calculate bid liquidity for each snapshot
    print("\nCalculating bid liquidity for each snapshot...")
    bid_liquidities = []
    
    for idx, row in df.iterrows():
        bid_liq = calculate_bid_liquidity(row)
        bid_liquidities.append(bid_liq)
    
    bid_liquidities = np.array(bid_liquidities)
    
    # Calculate statistics
    print("\n" + "=" * 80)
    print("OVERALL STATISTICS")
    print("=" * 80)
    print(f"Total snapshots: {len(bid_liquidities):,}")
    print(f"Average bid liquidity: ${np.mean(bid_liquidities):,.0f}")
    print(f"Median bid liquidity: ${np.median(bid_liquidities):,.0f}")
    print(f"Min bid liquidity: ${np.min(bid_liquidities):,.0f}")
    print(f"Max bid liquidity: ${np.max(bid_liquidities):,.0f}")
    print(f"Std deviation: ${np.std(bid_liquidities):,.0f}")
    
    # Distribution by ranges
    print("\n" + "=" * 80)
    print("LIQUIDITY DISTRIBUTION")
    print("=" * 80)
    print(f"{'Range':<20} {'Count':<15} {'Percentage':<12} {'Cumulative %':<15}")
    print("-" * 80)
    
    cumulative_pct = 0
    for min_val, max_val, label in RANGES:
        if max_val == float('inf'):
            count = np.sum(bid_liquidities >= min_val)
        else:
            count = np.sum((bid_liquidities >= min_val) & (bid_liquidities < max_val))
        
        percentage = (count / len(bid_liquidities) * 100) if len(bid_liquidities) > 0 else 0
        cumulative_pct += percentage
        
        print(f"{label:<20} {count:<15,} {percentage:<11.2f}% {cumulative_pct:<14.2f}%")
    
    # Show some example timestamps for low liquidity events
    print("\n" + "=" * 80)
    print("EXAMPLES OF LOW LIQUIDITY EVENTS (Under $10K)")
    print("=" * 80)
    
    low_liquidity_indices = np.where(bid_liquidities < 10000)[0]
    
    if len(low_liquidity_indices) > 0:
        print(f"Found {len(low_liquidity_indices):,} snapshots with bid liquidity under $10K")
        print("\nAll examples:")
        
        for i, idx in enumerate(low_liquidity_indices, 1):
            row = df.iloc[idx]
            timestamp_us = row['timestamp']
            utc_time = datetime.utcfromtimestamp(timestamp_us / 1_000_000)
            bid_liq = bid_liquidities[idx]
            
            print(f"  {i}. {utc_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC - ${bid_liq:,.0f}")
    else:
        print("No snapshots with bid liquidity under $10K in this time range")
    
    # Percentiles
    print("\n" + "=" * 80)
    print("PERCENTILES")
    print("=" * 80)
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        value = np.percentile(bid_liquidities, p)
        print(f"{p}th percentile: ${value:,.0f}")

if __name__ == "__main__":
    main()
