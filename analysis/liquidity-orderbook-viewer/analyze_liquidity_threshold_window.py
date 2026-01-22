import pandas as pd
import numpy as np
from datetime import datetime, timezone
import os
import glob

THRESHOLD = 10000  # $10K
START_TIME = datetime(2025, 10, 10, 20, 50, tzinfo=timezone.utc)
END_TIME = datetime(2025, 
10, 10, 21, 50, tzinfo=timezone.utc)
FOCUS_KEYS = {
    # "binance-futures_book_snapshot_25_2025-10-10_BTCUSDC",
    # "binance-futures_book_snapshot_25_2025-10-10_BTCUSDT",
}

def discover_datasets():
    """Automatically discover all CSV files in datasets folder for Oct 10 only."""
    datasets = {}

    day_folder = "Oct 10"
    folder_path = f"datasets/{day_folder}"
    if os.path.exists(folder_path):
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        csv_files = [f for f in csv_files if not f.endswith('.gz')]

        for filepath in csv_files:
            filename = os.path.basename(filepath)
            key = filename.replace('.csv', '')
            datasets[key] = filepath

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
    """Analyze a single file for bid liquidity below threshold within time window"""
    print(f"\n  Processing {name}...")

    chunk_size = 100000
    total_rows = 0
    below_threshold_count = 0
    below_threshold_times = []
    bid_liquidities = []

    try:
        for chunk in pd.read_csv(filepath, chunksize=chunk_size):
            for _, row in chunk.iterrows():
                timestamp_us = row['timestamp']
                utc_time = datetime.fromtimestamp(timestamp_us / 1_000_000, tz=timezone.utc)

                if utc_time < START_TIME or utc_time > END_TIME:
                    continue

                total_rows += 1
                bid_liq = calculate_bid_liquidity(row)
                bid_liquidities.append(bid_liq)

                if bid_liq < THRESHOLD:
                    below_threshold_count += 1
                    below_threshold_times.append({
                        'time': utc_time,
                        'bid_liquidity': bid_liq
                    })

        if total_rows == 0:
            raise ValueError("No snapshots within the selected time window")

        bid_liquidities = np.array(bid_liquidities)
        avg_bid = np.mean(bid_liquidities)
        min_bid = np.min(bid_liquidities)
        max_bid = np.max(bid_liquidities)

        below_threshold_pct = (below_threshold_count / total_rows * 100)

        result = {
            "total_rows": total_rows,
            "below_threshold": below_threshold_count,
            "below_threshold_pct": below_threshold_pct,
            "below_threshold_times": below_threshold_times,
            "avg_bid": avg_bid,
            "min_bid": min_bid,
            "max_bid": max_bid
        }

        print(f"    Total snapshots (window): {total_rows:,}")
        print(f"    Below ${THRESHOLD:,}: {below_threshold_count:,} ({below_threshold_pct:.2f}%)")
        print(f"    Avg bid liquidity: ${avg_bid:,.0f}")
        print(f"    Min: ${min_bid:,.0f} | Max: ${max_bid:,.0f}")

        if below_threshold_times:
            print(f"\n    All times below ${THRESHOLD:,}:")
            for i, event in enumerate(below_threshold_times, 1):
                print(f"      {i}. {event['time'].strftime('%Y-%m-%d %H:%M:%S')} UTC - ${event['bid_liquidity']:,.0f}")

        return result

    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def main():
    print("=" * 80)
    print("ALL EXCHANGES - BUY SIDE LIQUIDITY THRESHOLD (20:50–21:30 UTC)")
    print(f"Threshold: ${THRESHOLD:,}")
    print(f"Window: {START_TIME.strftime('%Y-%m-%d %H:%M')} to {END_TIME.strftime('%H:%M')} UTC")
    print("=" * 80)

    datasets = discover_datasets()
    if FOCUS_KEYS:
        datasets = {k: v for k, v in datasets.items() if k in FOCUS_KEYS}

    print(f"\nFound {len(datasets)} datasets (Oct 10):")
    for name in sorted(datasets.keys()):
        print(f"  - {name}")

    all_results = {}

    for name in sorted(datasets.keys()):
        result = analyze_file(name, datasets[name])
        if result:
            all_results[name] = result

    print("\n" + "=" * 80)
    print(f"SUMMARY - Times Below ${THRESHOLD:,} Threshold (Window)")
    print("=" * 80)

    for name in sorted(all_results.keys()):
        result = all_results[name]
        print(f"\n{name}:")
        print(f"  Snapshots: {result['total_rows']:,}")
        print(f"  Below ${THRESHOLD:,}: {result['below_threshold']:,} ({result['below_threshold_pct']:.2f}%)")
        print(f"  Avg bid: ${result['avg_bid']:,.0f} | Min: ${result['min_bid']:,.0f} | Max: ${result['max_bid']:,.0f}")

if __name__ == "__main__":
    main()
