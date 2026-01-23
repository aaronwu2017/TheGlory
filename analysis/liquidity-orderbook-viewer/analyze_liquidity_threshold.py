import pandas as pd
import numpy as np
from datetime import datetime, timezone
import os
import glob

THRESHOLD = 10000  # $10K

def discover_datasets():
    """Automatically discover all CSV files in datasets folder"""
    datasets = {}
    
    for day_folder in ["Oct 9", "Oct 10"]:
        folder_path = f"datasets/{day_folder}"
        if os.path.exists(folder_path):
            csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
            # Filter out .gz files
            csv_files = [f for f in csv_files if not f.endswith('.gz')]
            
            for filepath in csv_files:
                filename = os.path.basename(filepath)
                # Use filename as key (without .csv extension)
                key = filename.replace('.csv', '')
                
                if key not in datasets:
                    datasets[key] = {}
                
                datasets[key][day_folder] = filepath
    
    return datasets

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

def analyze_file(name, filepath):
    """Analyze a single file for bid liquidity below threshold"""
    print(f"\n  Processing {name}...")
    
    chunk_size = 100000
    total_rows = 0
    below_threshold_count = 0
    below_threshold_times = []
    bid_liquidities = []
    
    try:
        for chunk in pd.read_csv(filepath, chunksize=chunk_size):
            total_rows += len(chunk)
            
            # Calculate bid liquidity for each row
            for idx, row in chunk.iterrows():
                bid_liq = calculate_bid_liquidity(row)
                bid_liquidities.append(bid_liq)
                
                if bid_liq < THRESHOLD:
                    below_threshold_count += 1
                    # Convert timestamp to UTC
                    timestamp_us = row['timestamp']
                    utc_time = datetime.fromtimestamp(timestamp_us / 1_000_000, tz=timezone.utc)
                    below_threshold_times.append({
                        'time': utc_time,
                        'bid_liquidity': bid_liq
                    })
        
        # Calculate statistics
        bid_liquidities = np.array(bid_liquidities)
        avg_bid = np.mean(bid_liquidities)
        min_bid = np.min(bid_liquidities)
        max_bid = np.max(bid_liquidities)
        
        below_threshold_pct = (below_threshold_count / total_rows * 100) if total_rows > 0 else 0
        
        result = {
            "total_rows": total_rows,
            "below_threshold": below_threshold_count,
            "below_threshold_pct": below_threshold_pct,
            "below_threshold_times": below_threshold_times,
            "avg_bid": avg_bid,
            "min_bid": min_bid,
            "max_bid": max_bid
        }
        
        print(f"    Total snapshots: {total_rows:,}")
        print(f"    Below ${THRESHOLD:,}: {below_threshold_count:,} ({below_threshold_pct:.2f}%)")
        print(f"    Avg bid liquidity: ${avg_bid:,.0f}")
        print(f"    Min: ${min_bid:,.0f} | Max: ${max_bid:,.0f}")
        
        # Show first 10 times below threshold
        if below_threshold_times:
            print(f"\n    First 10 times below ${THRESHOLD:,}:")
            for i, event in enumerate(below_threshold_times[:10], 1):
                print(f"      {i}. {event['time'].strftime('%Y-%m-%d %H:%M:%S')} UTC - ${event['bid_liquidity']:,.0f}")
            
            if len(below_threshold_times) > 10:
                print(f"      ... and {len(below_threshold_times) - 10} more times")
        
        return result
    
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def analyze_exchange(name, files):
    """Analyze exchange across available days"""
    print(f"\nAnalyzing {name}...")
    
    results = {}
    
    for day in ["Oct 9", "Oct 10"]:
        if day in files:
            result = analyze_file(day, files[day])
            if result:
                results[day] = result
    
    return results

def main():
    print("=" * 80)
    print(f"ALL EXCHANGES - BUY SIDE LIQUIDITY THRESHOLD ANALYSIS")
    print(f"Threshold: ${THRESHOLD:,}")
    print("=" * 80)
    
    # Discover all datasets
    datasets = discover_datasets()
    
    print(f"\nFound {len(datasets)} datasets:")
    for name in sorted(datasets.keys()):
        days = list(datasets[name].keys())
        print(f"  - {name} ({', '.join(days)})")
    
    all_results = {}
    
    for name in sorted(datasets.keys()):
        results = analyze_exchange(name, datasets[name])
        if results:
            all_results[name] = results
    
    # Summary comparison
    print("\n" + "=" * 80)
    print(f"SUMMARY - Times Below ${THRESHOLD:,} Threshold")
    print("=" * 80)
    
    for name in sorted(all_results.keys()):
        results = all_results[name]
        oct9 = results.get("Oct 9", {})
        oct10 = results.get("Oct 10", {})
        
        print(f"\n{name}:")
        if oct9:
            print(f"  Oct 9:  {oct9.get('below_threshold', 0):,} times ({oct9.get('below_threshold_pct', 0):.2f}%)")
        if oct10:
            print(f"  Oct 10: {oct10.get('below_threshold', 0):,} times ({oct10.get('below_threshold_pct', 0):.2f}%)")
        
        if oct9 and oct10:
            change = oct10.get('below_threshold_pct', 0) - oct9.get('below_threshold_pct', 0)
            print(f"  Change: {change:+.2f}%")

if __name__ == "__main__":
    main()
