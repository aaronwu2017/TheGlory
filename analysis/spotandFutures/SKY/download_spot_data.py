from tardis_dev import datasets
import logging
import os
import pandas as pd
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

logging.basicConfig(level=logging.DEBUG)

EXCHANGES = ["binance", "coinbase", "gemini"]

SYMBOL_MAP = {
    "binance": ["SKYUSDT"],
    "coinbase": ["SKY-USD"],
    "gemini": ["SKYUSD"],
}

def download_spot_trades():
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Starting SKY spot trade data downloads...")
    print(f"Note: SKY may not be available on Coinbase")

    for exchange in EXCHANGES:
        exchange_symbols = SYMBOL_MAP.get(exchange, [])
        for symbol in exchange_symbols:
            try:
                datasets.download(
                    exchange=exchange,
                    data_types=["trades"],
                    from_date="2025-10-10",
                    to_date="2025-10-11",
                    symbols=[symbol],
                    api_key=api_key,
                    download_dir=os.path.join(script_dir, exchange)
                )
                print(f"✓ {exchange.upper()} download completed: {symbol}")
                break
            except Exception as e:
                print(f"✗ {exchange.upper()} error ({symbol}): {e}")

if __name__ == "__main__":
    download_spot_trades()
