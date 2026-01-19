# DOGE Spot Trading Analysis

Compare DOGE spot prices across major exchanges on 2025-10-10.

## Files
- `download_doge_data.py` – download and compare DOGE spot trades
- Exchange subfolders will be created on first run (binance, okex, bitfinex, coinbase, kraken, gemini, bybit, kucoin, gate-io, bitget)

## Usage
```bash
python download_doge_data.py
```

## Notes
- Symbols mapped per exchange (DOGEUSDT, DOGE-USDT, DOGE-USD, XDGUSD, etc.).
- Data and script live in this `DOGE/` folder; downloads are saved alongside per-exchange subfolders.
- Requires `tardis-dev`, `pandas`, and a valid Tardis API key (configured in the script).
