# AAVE Spot Trading Analysis

Compare AAVE spot prices across major exchanges on 2025-10-10.

## Files
- `download_aave_data.py` – download and compare AAVE spot trades
- Exchange subfolders will be created on first run (binance, okex, bitfinex, coinbase, kraken, gemini, bybit, kucoin, gate-io, bitget)

## Usage
```bash
python download_aave_data.py
```

## Notes
- Symbols mapped per exchange (AAVEUSDT, AAVE-USDT, AAVE-USD, AAVEUSD, etc.).
- Data and script live in this `AAVE/` folder; downloads are saved alongside per-exchange subfolders.
- Requires `tardis-dev`, `pandas`, and a valid Tardis API key (configured in the script).
