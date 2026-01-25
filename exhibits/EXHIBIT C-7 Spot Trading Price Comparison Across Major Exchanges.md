# EXHIBIT C-7: Spot Trading Price Comparison Across Major Exchanges

Compare spot trading prices across major exchanges (Binance, Coinbase, Gemini) during the October 10, 2025 incident.

## Coins Analyzed

- **BTC** (Bitcoin)
- **DOGE** (Dogecoin)
- **AAVE** (Aave)
- **SOL** (Solana)
- **POL** (Polygon)
- **CRV** (Curve)
- **WIF** (dogwifhat)
- **PEPE** (Pepe)
- **SKY** (Sky)
- **ENA** (Ethena)
- **BONK** (Bonk)
- **WLD** (Worldcoin)

## Exchanges

- **Binance** - Baseline reference
- **Coinbase** - US-regulated exchange
- **Gemini** - US-regulated exchange

## Results (2025-10-10)

| Coin | Binance Min | Coinbase Min | vs Binance | Gemini Min | vs Binance |
|------|-------------|--------------|------------|------------|------------|
| **BTC** | 102,000.00 | 107,000.00 | +4.9% | 107,000.00 | +4.9% |
| **SOL** | 168.79 | 176.85 | +4.8% | 172.10 | +2.0% |
| **DOGE** | 0.095 | 0.15 | +57.9% | 0.18188 | +91.5% |
| **AAVE** | 79.51 | 128.00 | +61.0% | 178.34 | +124.3% |
| **POL** | 0.1152 | - | - | 0.20 | +73.6% |
| **SKY** | 0.03491 | 0.03489 | -0.06% | 0.054114 | +55.0% |
| **PEPE** | 0.000003 | 0.000005 | +79.6% | 0.000006 | +100.5% |
| **BONK** | 0.000004 | 0.000013 | +220.9% | 0.000007 | +71.1% |
| **ENA** | 0.1313 | 0.282 | +114.8% | - | - |
| **CRV** | 0.1805 | 0.489 | +170.9% | 0.460 | +154.8% |
| **WLD** | 0.264 | 0.880 | **+233.3%** | - | - |
| **WIF** | 0.062 | 0.320 | **+416.1%** | 0.1454 | +134.5% |

**Conclusion:** During the October 10, 2025 incident, Binance spot prices for altcoins were severely depressed compared to US-regulated exchanges.

## Source Data

Analysis scripts and raw data files available in: `analysis/spot/`

- `compare_all_exchanges.py` - Main comparison script
- Individual coin folders with download scripts and CSV data
