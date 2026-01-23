from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import os

app = Flask(__name__)

# Load the CSV files
EXCHANGES = {
    "binance-usdt": {
        "path": "datasets/Oct 10/binance-futures_book_snapshot_25_2025-10-10_BTCUSDT.csv",
        "name": "Binance Futures",
        "symbol": "BTCUSDT",
        "available": True
    },
    "okx-usdt": {
        "path": "datasets/Oct 10/okex-swap_book_snapshot_25_2025-10-10_BTC-USDT-SWAP.csv",
        "name": "OKX Swap",
        "symbol": "BTC-USDT-SWAP",
        "available": True
    },
    "okx-usdc": {
        "path": "datasets/Oct 10/okex-swap_book_snapshot_25_2025-10-10_BTC-USDC-SWAP.csv",
        "name": "OKX Swap",
        "symbol": "BTC-USDC-SWAP",
        "available": True
    },
    "huobi-usdt": {
        "path": "datasets/Oct 10/huobi-dm-linear-swap_book_snapshot_25_2025-10-10_BTC-USDT.csv",
        "name": "Huobi Linear Swap",
        "symbol": "BTC-USDT",
        "available": True
    },
    "bybit-usdt": {
        "path": "datasets/Oct 10/bybit_book_snapshot_25_2025-10-10_BTCPERP.csv",
        "name": "Bybit",
        "symbol": "BTCPERP",
        "available": True
    },
    "bybit-usdc": {
        "name": "Bybit",
        "symbol": "BTCUSDC",
        "available": False  # Bybit doesn't have USDC perpetuals
    },
    "kucoin-usdt": {
        "path": "datasets/Oct 10/kucoin-futures_book_snapshot_25_2025-10-10_XBTUSDTM.csv",
        "name": "KuCoin Futures",
        "symbol": "XBTUSDTM",
        "available": False  # Excluded - file too large (30GB, 52M rows)
    },
    "kucoin-usdc": {
        "path": "datasets/Oct 10/kucoin-futures_book_snapshot_25_2025-10-10_XBTUSDCM.csv",
        "name": "KuCoin Futures",
        "symbol": "XBTUSDCM",
        "available": True
    },
    "hyperliquid": {
        "path": "datasets/Oct 10/hyperliquid_book_snapshot_25_2025-10-10_BTC.csv",
        "name": "Hyperliquid",
        "symbol": "BTC",
        "available": True
        # Note: Hyperliquid does not specify whether this is USDT or USDC based
    },
    "bitget-usdt": {
        "path": "datasets/Oct 10/bitget-futures_book_snapshot_25_2025-10-10_BTCUSDT.csv",
        "name": "Bitget Futures",
        "symbol": "BTCUSDT",
        "available": True
    },
    "bitget-usdc": {
        "path": "datasets/Oct 10/bitget-futures_book_snapshot_25_2025-10-10_BTCUSDC.csv",
        "name": "Bitget Futures",
        "symbol": "BTCUSDC",
        "available": False  # File not downloaded yet
    },
    "coinbase-usdt": {
        "path": "datasets/Oct 10/coinbase-international_book_snapshot_25_2025-10-10_BTC-PERP.csv",
        "name": "Coinbase International",
        "symbol": "BTC-PERP",
        "available": True
        # Note: Coinbase does not specify whether this is USDT or USDC based
    },
    "coinbase-usdc": {
        "name": "Coinbase International",
        "symbol": "BTC-PERP-USDC",
        "available": False  # Coinbase doesn't have USDC perpetuals
    },
    "binance-usdc": {
        "path": "datasets/Oct 10/binance-futures_book_snapshot_25_2025-10-10_BTCUSDC.csv",
        "name": "Binance Futures",
        "symbol": "BTCUSDC",
        "available": True
    },
    "huobi-usdc": {
        "name": "Huobi Linear Swap",
        "symbol": "BTC-USDC",
        "available": False
    }
}

# Cache for loaded data (per exchange)
data_cache = {}

# Baseline liquidity from Oct 9 (calculated once)
BASELINE_LIQUIDITY = {
    "binance-usdt": {"bid": 1448792, "ask": 1550777, "total": 2999570},
    "binance-usdc": {"bid": 1448792, "ask": 1550777, "total": 2999570},  # Same as USDT
    "okx-usdt": {"bid": 155350553, "ask": 138620529, "total": 293971083},
    "okx-usdc": {"bid": 155350553, "ask": 138620529, "total": 293971083},  # Same as USDT
    "bybit-usdt": {"bid": 312472, "ask": 231165, "total": 543637},
    "huobi-usdt": {"bid": 1244267512, "ask": 1167725660, "total": 2411993171},
    "kucoin-usdc": {"bid": 2183802634, "ask": 2930176358, "total": 5113978992},
    "hyperliquid": {"bid": 3939981, "ask": 5221660, "total": 9161641},
    "bitget-usdt": {"bid": 4048468, "ask": 4114361, "total": 8162829},
    "coinbase-usdt": {"bid": 1443318, "ask": 1415861, "total": 2859179},
}


@app.route("/")
def index():
    return render_template("orderbook.html")


def load_data_cache(exchange):
    """Load data into cache if not already loaded"""
    if exchange not in EXCHANGES:
        print(f"ERROR: Unknown exchange: {exchange}")
        print(f"Available exchanges: {list(EXCHANGES.keys())}")
        raise ValueError(f"Unknown exchange: {exchange}")
    
    # Check if data is available for this exchange
    if not EXCHANGES[exchange].get("available", True):
        print(f"INFO: Exchange {exchange} is marked as unavailable")
        raise FileNotFoundError(f"No data available for {EXCHANGES[exchange]['name']} with {EXCHANGES[exchange]['symbol']}")
    
    if exchange not in data_cache:
        print(f"Loading {exchange} CSV into memory...")
        csv_path = EXCHANGES[exchange]["path"]
        print(f"CSV path: {csv_path}")
        
        if not os.path.exists(csv_path):
            print(f"ERROR: File does not exist: {csv_path}")
            raise FileNotFoundError(f"Data file not found: {csv_path}. Please download the data first.")
        
        try:
            data_cache[exchange] = {
                "df": pd.read_csv(csv_path),
                "timestamps": None
            }
            data_cache[exchange]["timestamps"] = data_cache[exchange]["df"]["timestamp"].values
            print(f"Loaded {len(data_cache[exchange]['df'])} rows for {exchange}")
        except Exception as e:
            print(f"ERROR loading {exchange}: {e}")
            raise FileNotFoundError(f"Error loading data file: {csv_path}. Error: {e}")
    else:
        print(f"Using cached data for {exchange}")


@app.route("/api/data")
def get_data():
    try:
        # Get parameters
        exchange = request.args.get("exchange", "binance-usdt")
        start_row = int(request.args.get("start", 0))
        
        load_data_cache(exchange)
        
        df = data_cache[exchange]["df"]
        
        if start_row >= len(df) or start_row < 0:
            return jsonify({"error": "Row out of range"})
        
        # Get the specific row
        row = df.iloc[start_row]
        
        # Extract bids and asks
        bids = []
        asks = []
        bid_liquidity = 0
        ask_liquidity = 0
        
        for i in range(25):
            bid_price = row.get(f"bids[{i}].price")
            bid_amount = row.get(f"bids[{i}].amount")
            ask_price = row.get(f"asks[{i}].price")
            ask_amount = row.get(f"asks[{i}].amount")
            
            if pd.notna(bid_price) and pd.notna(bid_amount):
                bids.append({"price": float(bid_price), "amount": float(bid_amount)})
                bid_liquidity += float(bid_price) * float(bid_amount)
            if pd.notna(ask_price) and pd.notna(ask_amount):
                asks.append({"price": float(ask_price), "amount": float(ask_amount)})
                ask_liquidity += float(ask_price) * float(ask_amount)
        
        # Get baseline liquidity for this exchange
        baseline = BASELINE_LIQUIDITY.get(exchange, {"bid": 0, "ask": 0, "total": 0})
        
        return jsonify({
            "timestamp": int(row["timestamp"]),
            "symbol": str(row["symbol"]),
            "bids": bids,
            "asks": asks,
            "current_row": int(start_row),
            "total_rows": int(len(df)),
            "current_liquidity": {
                "bid": bid_liquidity,
                "ask": ask_liquidity,
                "total": bid_liquidity + ask_liquidity
            },
            "baseline_liquidity": baseline
        })
    except FileNotFoundError as e:
        return jsonify({"error": "No data available", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error loading data: {str(e)}"}), 500


@app.route("/api/find-timestamp")
def find_timestamp():
    try:
        exchange = request.args.get("exchange", "binance-usdt")
        target_timestamp = int(request.args.get("timestamp", 0))
        
        load_data_cache(exchange)
        
        # Use numpy for fast search
        timestamps = data_cache[exchange]["timestamps"]
        closest_idx = abs(timestamps - target_timestamp).argmin()
        
        return jsonify({
            "row": int(closest_idx),
            "timestamp": int(timestamps[closest_idx])
        })
    except FileNotFoundError as e:
        return jsonify({"error": "No data available", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error finding timestamp: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5002)
