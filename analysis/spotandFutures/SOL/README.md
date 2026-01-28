# SOL Spot Trading Analysis

Compare SOL spot prices across major exchanges on 2025-10-10.

## Files
- `download_sol_data.py` – download and compare SOL spot trades
- Exchange subfolders will be created on first run (binance, okex, bitfinex, coinbase, kraken, gemini, bybit, kucoin, gate-io, bitget)

## Usage
```bash
python download_sol_data.py
```

## Notes
- Symbols mapped per exchange (SOLUSDT, SOL-USDT, SOL-USD, SOLUSD, etc.).
- Data and script live in this `SOL/` folder; downloads are saved alongside per-exchange subfolders.
- Requires `tardis-dev`, `pandas`, and a valid Tardis API key (configured in the script).
