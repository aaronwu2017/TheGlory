import pandas as pd
import os
import numpy as np
import glob

def load_binance_data(binance_path, extra_files=None):
    """
    Reads Binance ZIP files, cleans timestamps and returns DataFrame with 'low' column.
    """
    print(f"--- Loading Binance Data ---")
    print(f"Binance Path: {os.path.relpath(binance_path)}")

    try:
        # Define Binance ZIP file column names (no header)
        binance_cols = [
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_volume', 'count', 'taker_buy_volume', 
            'taker_buy_quote_volume', 'ignore'
        ]

        # Read all zip files in the directory
        zip_files = sorted(glob.glob(os.path.join(binance_path, "*.zip")))
        print(f"Found {len(zip_files)} ZIP files in Binance directory.")
        
        if not zip_files:
            raise ValueError("No .zip files found in the specified directory.")

        df_list = []
        for zf in zip_files:
            # Read csv inside zip, no header
            temp_df = pd.read_csv(zf, compression='zip', header=None, names=binance_cols)
            df_list.append(temp_df)
        
        df_binance = pd.concat(df_list, ignore_index=True)

        # Clean data: remove potential header rows (when merging multiple files with headers)
        if 'open_time' in df_binance.columns:
            # Filter out rows with value 'open_time' (prevent reading CSV header)
            df_binance = df_binance[df_binance['open_time'].astype(str) != 'open_time']
            # Convert to numeric
            df_binance['open_time'] = pd.to_numeric(df_binance['open_time'])
            
            # Binance ZIP format is usually 'open_time' and ms Unix timestamp
            df_binance['time'] = pd.to_datetime(df_binance['open_time'], unit='ms')
        elif 'time' in df_binance.columns:
            df_binance['time'] = pd.to_datetime(df_binance['time'])
        else:
            raise ValueError("Time column not found in Binance data (open_time or time)")

        if 'low' not in df_binance.columns:
            raise ValueError("Binance data missing 'low' column")

        df_binance['low'] = pd.to_numeric(df_binance['low'], errors='coerce')
        df_binance['close'] = pd.to_numeric(df_binance['close'], errors='coerce')
        df_binance['time'] = df_binance['time'].dt.floor('s')

        df_binance.set_index('time', inplace=True)
        df_binance.sort_index(inplace=True)

        df_final = df_binance[['low', 'close']]

        # Process extra CSV files (e.g. BINANCE_BTCUSD, 10.csv)
        if extra_files:
            for f in extra_files:
                if os.path.exists(f):
                    try:
                        print(f"Loading extra Binance file: {os.path.basename(f)}")
                        df_extra = pd.read_csv(f)
                        df_extra.columns = [c.strip().lower() for c in df_extra.columns]
                        if 'time' in df_extra.columns and 'low' in df_extra.columns:
                            df_extra['time'] = pd.to_datetime(df_extra['time'])
                            
                            # Handle timezone: convert to UTC then remove tz info to match naive timestamps from ZIPs
                            if df_extra['time'].dt.tz is not None:
                                df_extra['time'] = df_extra['time'].dt.tz_convert('UTC').dt.tz_localize(None)
                            
                            df_extra['time'] = df_extra['time'].dt.floor('s')
                            df_extra['low'] = pd.to_numeric(df_extra['low'], errors='coerce')
                            df_extra.set_index('time', inplace=True)
                            df_final = pd.concat([df_final, df_extra[['low']]])
                    except Exception as e:
                        print(f"Error loading extra file {f}: {e}")
        
        df_final.sort_index(inplace=True)
        # Remove duplicates if any
        df_final = df_final[~df_final.index.duplicated(keep='first')]
        
        return df_final

    except Exception as e:
        print(f"Error loading Binance data: {e}")
        return None

def align_etf_data(etf_path, df_binance, etf_name):
    """
    Reads ETF CSV, cleans and aligns with pre-loaded Binance data.
    """
    print(f"--- Processing {etf_name} Data ---")
    print(f"{etf_name} Path: {os.path.relpath(etf_path)}")

    try:
        df_etf = pd.read_csv(etf_path)
        df_etf.columns = [c.strip().lower() for c in df_etf.columns]

        if 'time' not in df_etf.columns:
             raise ValueError(f"Missing column in {etf_name} file: time")
        
        # Determine ETF time format
        if pd.api.types.is_numeric_dtype(df_etf['time']):
            first_ts = df_etf['time'].iloc[0]
            if first_ts > 1e11:
                df_etf['time'] = pd.to_datetime(df_etf['time'], unit='ms')
            else:
                df_etf['time'] = pd.to_datetime(df_etf['time'], unit='s')
        else:
            df_etf['time'] = pd.to_datetime(df_etf['time'])

        if 'low' not in df_etf.columns:
            raise ValueError(f"{etf_name} data missing 'low' column")
        if 'close' not in df_etf.columns:
            raise ValueError(f"{etf_name} data missing 'close' column")

        df_etf['low'] = pd.to_numeric(df_etf['low'], errors='coerce')
        df_etf['close'] = pd.to_numeric(df_etf['close'], errors='coerce')
        df_etf['time'] = df_etf['time'].dt.floor('s')

        df_etf.set_index('time', inplace=True)
        df_etf.sort_index(inplace=True)

        print(f"Original data rows: {etf_name} = {len(df_etf)}, Binance = {len(df_binance)}")

        # Use concat for inner join, keeping both Low and Close
        aligned_data = pd.concat(
            [df_etf['low'], df_binance['low'], df_etf['close'], df_binance['close']], 
            axis=1, 
            keys=[etf_name, 'Binance', f'{etf_name}_close', 'Binance_close']
        )
        
        # Drop rows with null values (ensure data is fully aligned)
        aligned_data.dropna(inplace=True)

        return aligned_data

    except FileNotFoundError:
        print(f"File not found: {etf_path}")
        return None
    except Exception as e:
        print(f"Error processing {etf_name}: {e}")
        return None

def perform_analysis(aligned_data, is_specific=False):
    """
    Receives aligned DataFrame, calculates Pearson correlation, rolling correlation, and outputs analysis report.
    """
    if aligned_data is None or aligned_data.empty:
        print("Error: Data is empty, cannot perform analysis.")
        return

    # Identify ETF column name (the one that is not 'Binance')
    cols = aligned_data.columns
    # Filter for the main ETF low column (exclude Binance and any _close columns)
    etf_col = [c for c in cols if c != 'Binance' and not c.endswith('_close') and not c.startswith('Binance')][0]
    
    data_count = len(aligned_data)
    print(f"Analyzing {data_count} data points for {etf_col} vs Binance...")
    if data_count > 0:
        print(f"Data Time Range: {aligned_data.index[0]} to {aligned_data.index[-1]}")

    # 4. Calculate Pearson Correlation
    # Method A: Use pandas built-in function (Recommended, optimized)
    r_pandas = aligned_data[etf_col].corr(aligned_data['Binance'], method='pearson')

    # --- New: Global Anomaly Scan (Find other pump/dump periods) ---
    anomaly_report = []
    anomalies_15m_ratios = []
    # Run scan only when data is sufficient (e.g., > half day), avoid repetition in short windows
    if data_count > 100 or is_specific:
        # Define scan windows list: (window size, label)
        # 3 points = 15 mins, 12 points = 1 hour
        scan_windows = [(3, "15m"), (12, "1h")]
        
        for window_scan, label in scan_windows:
            pct_etf = aligned_data[etf_col].pct_change(periods=window_scan)
            pct_binance = aligned_data['Binance'].pct_change(periods=window_scan)
            
            scan_df = pd.DataFrame({etf_col: pct_etf, 'Binance': pct_binance})
            
            # Filter conditions:
            # 1. Binance absolute volatility > 1% (Ensure significant movement)
            # 2. Binance magnitude > 1.5 * ETF magnitude (Significant pump/dump)
            mask = (scan_df['Binance'].abs() > 0.01) & \
                   (scan_df['Binance'].abs() > scan_df[etf_col].abs() * 1.5)
            
            anomalies = scan_df[mask]
            
            # Deduplication logic: Avoid printing consecutive points of the same trend (Set 2-hour cooldown)
            last_time = None
            for t, row in anomalies.iterrows():
                if last_time is None or (t - last_time).total_seconds() > 3600 * 2: 
                    # --- Filter Logic: Exclude overnight gaps and market open data ---
                    
                    # 1. Exclude overnight/cross-session data (Large time difference)
                    curr_idx = aligned_data.index.get_loc(t)
                    prev_idx = curr_idx - window_scan
                    if prev_idx >= 0:
                        prev_t = aligned_data.index[prev_idx]
                        # If time diff > window time (s) + 5 min tolerance, indicates a gap
                        if (t - prev_t).total_seconds() > (window_scan * 300 + 300):
                            continue

                    # 2. Exclude US Market Open times (13:30 UTC or 14:30 UTC)
                    if (t.hour == 13 or t.hour == 14) and t.minute == 30:
                        continue

                    ratio = row['Binance'] / row[etf_col] if row[etf_col] != 0 else 0
                    etype = "Drop" if row['Binance'] < 0 else "Pump"
                    report_line = f"[{label}] {str(t):<20} Binance:{row['Binance']*100:>6.2f}% vs {etf_col}:{row[etf_col]*100:>6.2f}% (倍数:{abs(ratio):.1f}x) - {etype}"
                    anomaly_report.append(report_line)
                    if label == "15m":
                        anomalies_15m_ratios.append(abs(ratio))
                    last_time = t

    # --- New: Calculate Global 15-min Volatility Multiplier ---
    # 15 mins = 3 * 5 mins
    window_stats = 3 
    s_etf = aligned_data[etf_col].pct_change(periods=window_stats)
    s_binance = aligned_data['Binance'].pct_change(periods=window_stats)
    
    # Filter valid volatility (ETF > 0.05%), avoid noise and division by zero
    mask_valid = s_etf.abs() > 0.0005
    valid_count = mask_valid.sum()
    
    avg_ratio = 0.0
    median_ratio = 0.0
    
    if valid_count > 0:
        # Calculate multiplier: Binance magnitude / ETF magnitude
        ratios = s_binance[mask_valid].abs() / s_etf[mask_valid].abs()
        avg_ratio = ratios.mean()
        median_ratio = ratios.median()

    # 5. Output Results
    if not is_specific:
        print("-" * 40)
        print(f"Advanced Analysis ({etf_col} vs Binance):")
        
        print(f"Global Volatility Multiplier (15-min window, samples={valid_count}):")
        if valid_count > 0:
            print(f"  -> Avg Multiplier: {avg_ratio:.2f}x (Binance volatility is usually {avg_ratio:.2f}x of {etf_col})")
            print(f"  -> Median Multiplier: {median_ratio:.2f}x")
        else:
            print("  -> Volatility too small to calculate valid multiplier")
        print("-" * 40)
    
    # Output anomaly scan results
    if not is_specific:
        if anomaly_report:
            print(f">>> Historical Anomaly Scan (15m & 1h | Binance Vol > 1% & Mag > 1.5x {etf_col}) <<<")
            print(f"Found {len(anomaly_report)} significant independent events:")
            for line in anomaly_report:
                print(line)
            print("-" * 40)
        elif data_count > 100:
            print(">>> Historical Anomaly Scan: No other significant pump/dump events found.")
            print("-" * 40)
    
    # Drop/Rise Analysis
    if data_count > 0:
        print("Interval Price Change Analysis (Based on Low):")
        # Calculate drop from interval start price to lowest price
        etf_start = aligned_data[etf_col].iloc[0]
        etf_min = aligned_data[etf_col].min()
        etf_min_time = aligned_data[etf_col].idxmin()
        etf_drop_pct = (etf_min - etf_start) / etf_start * 100

        binance_start = aligned_data['Binance'].iloc[0]
        binance_min = aligned_data['Binance'].min()
        binance_min_time = aligned_data['Binance'].idxmin()
        binance_drop_pct = (binance_min - binance_start) / binance_start * 100

        print(f"{etf_col:<7} Max Drop: {etf_drop_pct:.2f}% (Start: {etf_start} -> Low: {etf_min} @ {etf_min_time})")
        print(f"Binance Max Drop: {binance_drop_pct:.2f}% (Start: {binance_start} -> Low: {binance_min} @ {binance_min_time})")
        
    print("-" * 40)

def calculate_theoretical_price(full_data, etf_name, crash_start_ts):
    """
    Calculates theoretical Binance price based on US Morning average ratio.
    """
    try:
        # Determine the date from the crash timestamp
        crash_date = pd.to_datetime(crash_start_ts, unit='s').tz_localize('UTC').tz_convert('America/New_York').date()
        
        # Define US Morning Window: 9:30 AM - 12:00 PM ET
        morning_start_et = pd.Timestamp(crash_date).tz_localize('America/New_York').replace(hour=9, minute=30)
        morning_end_et = pd.Timestamp(crash_date).tz_localize('America/New_York').replace(hour=12, minute=0)
        
        # Convert to UTC for filtering
        morning_start_utc = morning_start_et.tz_convert('UTC').tz_localize(None)
        morning_end_utc = morning_end_et.tz_convert('UTC').tz_localize(None)
        
        # Filter data
        morning_data = full_data.loc[morning_start_utc:morning_end_utc]
        
        if not morning_data.empty:
            # Calculate Ratio using CLOSE prices
            avg_ratio = (morning_data['Binance_close'] / morning_data[f'{etf_name}_close']).mean()
            print(f"Theoretical Price Analysis (Ref: US Morning {morning_start_et.time()} - {morning_end_et.time()} ET):")
            print(f"  -> Avg Conversion Ratio: {avg_ratio:.4f} (Binance / {etf_name})")
            return avg_ratio
        else:
            print("  -> Warning: No data found for US morning session to calculate ratio.")
            return None
    except Exception as e:
        print(f"  -> Error calculating theoretical price: {e}")
        return None

if __name__ == "__main__":
    # Configure Paths
    # Get script absolute path to ensure accurate location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # data folder is in the same directory as this file
    data_dir = os.path.join(script_dir, 'data')
    
    # Get absolute path for prettier output
    data_dir = os.path.abspath(data_dir)

    # Update to new filenames and directories
    file_ibit = os.path.join(data_dir, 'BATS_IBIT, 5_unix.csv')
    dir_binance = os.path.join(data_dir, 'binance data')

    # Load Binance Data Once
    df_binance = load_binance_data(dir_binance)
    if df_binance is not None:
        # --- Analysis 1: IBIT ---
        print("\n" + "="*20 + " IBIT Analysis " + "="*20)
        ibit_data = align_etf_data(file_ibit, df_binance, "IBIT")
        
        if ibit_data is not None:
            print("\n" + "="*20 + " Full Data Analysis (IBIT) " + "="*20)
            perform_analysis(ibit_data)

            # Calculate Ratio from Full Data (Morning Session)
            ibit_ratio = calculate_theoretical_price(ibit_data, "IBIT", 1760128200)

            print("\n" + "="*20 + " Specific Time Range Analysis (IBIT) " + "="*20)
            target_start = 1760128200
            target_end   = 1760135400
            print(f"Target Timestamp (Unix): {target_start} -> {target_end} (UTC: {pd.to_datetime(target_start, unit='s')} -> {pd.to_datetime(target_end, unit='s')})")
            
            st = pd.to_datetime(target_start, unit='s')
            et = pd.to_datetime(target_end, unit='s')
            sliced_ibit = ibit_data.loc[st:et]
            perform_analysis(sliced_ibit, is_specific=True)
            
            # Apply Ratio to Low
            if ibit_ratio and not sliced_ibit.empty:
                actual_ibit_low = sliced_ibit['IBIT'].min()
                actual_binance_low = sliced_ibit['Binance'].min()
                theoretical_binance = actual_ibit_low * ibit_ratio
                diff = actual_binance_low - theoretical_binance
                print(f"Theoretical Binance Low (based on morning ratio): {theoretical_binance:.2f}")
                print(f"Actual Binance Low: {actual_binance_low:.2f} (Diff: {diff:+.2f})")

        # --- Analysis 2: FBTC ---
        file_fbtc = os.path.join(data_dir, 'BATS_FBTC, 5.csv')
        print("\n" + "="*20 + " FBTC Analysis " + "="*20)
        fbtc_data = align_etf_data(file_fbtc, df_binance, "FBTC")
        
        if fbtc_data is not None:
            print("\n" + "="*20 + " Full Data Analysis (FBTC) " + "="*20)
            perform_analysis(fbtc_data)

            # Calculate Ratio from Full Data (Morning Session of the target date)
            fbtc_ratio = calculate_theoretical_price(fbtc_data, "FBTC", 1760128200)

            print("\n" + "="*20 + " Specific Time Range Analysis (FBTC) " + "="*20)
            # Using same time range as IBIT for comparison
            target_start = 1760128200
            target_end   = 1760135400
            print(f"Target Timestamp (Unix): {target_start} -> {target_end} (UTC: {pd.to_datetime(target_start, unit='s')} -> {pd.to_datetime(target_end, unit='s')})")
            
            st = pd.to_datetime(target_start, unit='s')
            et = pd.to_datetime(target_end, unit='s')
            
            # Check if data covers the target range
            if not fbtc_data.empty and (st > fbtc_data.index[-1] or et < fbtc_data.index[0]):
                print(f"WARNING: Target time range ({st} - {et}) is NOT in the loaded data range ({fbtc_data.index[0]} - {fbtc_data.index[-1]}).")
                print("Please ensure your CSV file contains data for the target date.")

            sliced_fbtc = fbtc_data.loc[st:et]
            perform_analysis(sliced_fbtc, is_specific=True)
            
            # Apply Ratio to Low
            if fbtc_ratio and not sliced_fbtc.empty:
                actual_fbtc_low = sliced_fbtc['FBTC'].min()
                actual_binance_low = sliced_fbtc['Binance'].min()
                theoretical_binance = actual_fbtc_low * fbtc_ratio
                diff = actual_binance_low - theoretical_binance
                print(f"Theoretical Binance Low (based on morning ratio): {theoretical_binance:.2f}")
                print(f"Actual Binance Low: {actual_binance_low:.2f} (Diff: {diff:+.2f})")
