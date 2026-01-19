# Spot Trading Data Analysis

Compare spot trading prices across major compliant exchanges (Coinbase, Kraken, Binance) during the October 10, 2025 incident.

## Files

- `download_spot_data.py` - Download and compare spot trade data
- `datasets_spot/` - Downloaded trade data (created on first run)

## Usage

```bash
python download_spot_data.py
```

## Output

- Downloads BTC spot trades from:
  - **Coinbase** (exchange: coinbase)
  - **Kraken** (exchange: kraken)
  - **Binance** (exchange: binance)

- Compares minimum prices across exchanges
- Calculates price differential vs Binance baseline

## Requirements

- `tardis-dev` (same as options folder)
- `pandas`
- Valid Tardis API key (configured in script)
