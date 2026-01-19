# Spot Trading Data Analysis

Compare spot trading prices across major exchanges (Binance, Coinbase, Gemini) during the October 10, 2025 incident.

## Files

- `compare_all_exchanges.py` - Compare prices across all coins and exchanges
- Individual coin folders with download scripts:
  - `BTC/download_spot_data.py`
  - `DOGE/download_doge_data.py`
  - `AAVE/download_aave_data.py`
  - `SOL/download_sol_data.py`
  - `POL/download_pol_data.py`

## Coins Analyzed

- **BTC** (Bitcoin)
- **DOGE** (Dogecoin)
- **AAVE** (Aave)
- **SOL** (Solana)
- **POL** (Polygon)

## Exchanges

- **Binance** - Baseline reference
- **Coinbase** - US-regulated exchange
- **Gemini** - US-regulated exchange

## Usage

Run the comparison script to analyze all coins:

```bash
cd analysis/spot
python compare_all_exchanges.py
```

## Results (2025-10-10)

```
BTC:
  Binance min 102000.00 (11,404,360 records)
  Coinbase min 107000.00 | vs Binance +4.9020%
  Gemini min 107000.00 | vs Binance +4.9020%

DOGE:
  Binance min 0.09500000 (5,176,557 records)
  Coinbase min 0.15000000 | vs Binance +57.8947%
  Gemini min 0.18188000 | vs Binance +91.4526%

AAVE:
  Binance min 79.510000 (690,659 records)
  Coinbase min 128.000000 | vs Binance +60.9860%
  Gemini min 178.341600 | vs Binance +124.3008%

SOL:
  Binance min 168.790000 (5,852,239 records)
  Coinbase min 176.850000 | vs Binance +4.7752%
  Gemini min 172.100000 | vs Binance +1.9610%

POL:
  Binance min 0.115200 (300,351 records)
  Coinbase min 0.150000 | vs Binance +30.2083%
  Gemini min 0.200000 | vs Binance +73.6111%
```

### Key Findings

- **BTC**: Minimal price difference (~5%) across all exchanges
- **SOL**: Relatively stable pricing across exchanges (~2-5% difference)
- **DOGE**: Significant variance (58-91% higher on US exchanges)
- **AAVE**: High variance (61-124% higher on US exchanges)
- **POL**: Moderate to high variance (30-74% higher on US exchanges)

## Requirements

- `tardis-dev`
- `pandas`
- Valid Tardis API key (configured in scripts)
