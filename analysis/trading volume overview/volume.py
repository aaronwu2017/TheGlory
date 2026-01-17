import pandas as pd
import os
from datetime import datetime, timedelta

def analyze_trading_volume():
    # ================= 配置区域 =================
    # 基础路径
    base_dir = r"C:\Users\aaron\OneDrive\Desktop\黑暗荣耀1011\analysis\trading volume overview"
    binance_dir = os.path.join(base_dir, "binance")
    ibit_path = os.path.join(base_dir, "ibit", "BATS_IBIT, D (1).csv")
    
    # 分析的日期范围
    start_date = "2025-10-01"
    end_date = "2025-10-09"

    # 读取 IBIT 数据
    print(f"Loading IBIT data from: {ibit_path}")
    try:
        df_ibit = pd.read_csv(ibit_path)
        df_ibit.columns = [c.strip().lower() for c in df_ibit.columns]
        
        # 处理时间列
        if 'time' in df_ibit.columns:
            # 判断是否为时间戳 (Daily 数据通常是字符串，但也可能是 Unix)
            if pd.api.types.is_numeric_dtype(df_ibit['time']) and df_ibit['time'].iloc[0] > 1e8:
                 df_ibit['dt'] = pd.to_datetime(df_ibit['time'], unit='s')
            else:
                 df_ibit['dt'] = pd.to_datetime(df_ibit['time'])
            
            df_ibit['date_str'] = df_ibit['dt'].dt.strftime("%Y-%m-%d")
            # 转为字典: date -> {open, volume}
            ibit_data = df_ibit.set_index('date_str')[['open', 'volume']].to_dict(orient='index')
        else:
            print("Error: 'time' column not found in IBIT CSV")
            return
    except Exception as e:
        print(f"Failed to load IBIT data: {e}")
        return

    print(f"{'Date':<12} | {'Binance Open':<12} | {'IBIT Open':<10} | {'Ratio (BTC/Share)':<18} | {'Binance Vol (BTC)':<18} | {'IBIT Vol (Eqv BTC)':<18} | {'Comparison (Binance/IBIT)'}")
    print("-" * 120)

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 检查是否有 IBIT 数据（跳过周末或节假日）
        if date_str not in ibit_data or ibit_data[date_str]["volume"] == 0:
            current_date += timedelta(days=1)
            continue

        # 处理币安数据 (同时查找 BTCUSDT 和 BTCUSDC)
        pairs = ["BTCUSDT", "BTCUSDC"]
        total_binance_vol = 0.0
        binance_open_price = 0.0
        found_binance_data = False

        # 计算时间戳范围
        day_start_ts = current_date.timestamp()
        market_open_ts = (day_start_ts + 13.5 * 3600) * 1000000
        market_close_ts = (day_start_ts + 20 * 3600) * 1000000

        for pair in pairs:
            # 构造文件名: BTCUSDT-aggTrades-2025-10-03.zip
            filename = f"{pair}-aggTrades-{date_str}.zip"
            file_path = os.path.join(binance_dir, filename)
            
            if not os.path.exists(file_path):
                continue

            try:
                # 读取 ZIP 中的 CSV
                df = pd.read_csv(
                    file_path, 
                    compression='zip',
                    header=None, 
                    usecols=[1, 2, 5], 
                    names=['price', 'qty', 'timestamp']
                )
                
                # 过滤数据
                market_data = df[(df['timestamp'] >= market_open_ts) & (df['timestamp'] <= market_close_ts)]
                
                if not market_data.empty:
                    found_binance_data = True
                    total_binance_vol += market_data['qty'].sum()
                    
                    # 优先使用 BTCUSDT 的开盘价，或者如果还没找到价格
                    if pair == "BTCUSDT" or (binance_open_price == 0):
                        binance_open_price = market_data.iloc[0]['price']
            
            except Exception as e:
                print(f"Error reading {pair} for {date_str}: {e}")

        if not found_binance_data:
            print(f"{date_str} | No Binance data found (checked USDT/USDC zips)")
            current_date += timedelta(days=1)
            continue

        # 3. 获取 IBIT 数据
        ibit_open_price = ibit_data[date_str]["open"]
        ibit_volume_shares = ibit_data[date_str]["volume"]

        # 4. 计算换算比例 (1 IBIT share = ? BTC)
        # 逻辑：如果在开盘时买入 1 股 IBIT，相当于买入了 (IBIT价格 / BTC价格) 个 BTC
        ratio = ibit_open_price / binance_open_price

        # 5. 计算 IBIT 等效 BTC 交易量
        ibit_volume_btc_eqv = ibit_volume_shares * ratio

        # 6. 对比
        comparison = total_binance_vol / ibit_volume_btc_eqv if ibit_volume_btc_eqv > 0 else 0

        print(f"{date_str} | ${binance_open_price:<11.2f} | ${ibit_open_price:<9.2f} | {ratio:.8f} BTC      | {total_binance_vol:<18.2f} | {ibit_volume_btc_eqv:<18.2f} | {comparison:.2f}x")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    analyze_trading_volume()
