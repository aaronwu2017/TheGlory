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
- **ATOM** (Cosmos)

## Exchanges

- **Binance** - Baseline reference
- **Coinbase** - US-regulated exchange
- **Gemini** - US-regulated exchange

## Results (2025-10-10)

### Spot Trading Minimum Prices

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
| **ATOM** | **0.001** | 3.00 | **+299,900%** | 3.00 | **+299,900%** |

---

### Binance Coin-Margined Futures (COIN-M) Minimum Prices

Coin-margined perpetual contracts also experienced extreme price anomalies during the incident:

| Coin | COIN-M Min | COIN-M Max | Drop % |
|------|------------|------------|--------|
| **BTC** | 101,389.70 | 122,531.30 | -17.3% |
| **ETH** | 3,378.19 | 4,394.64 | -23.1% |
| **SOL** | 137.21 | 224.41 | -38.9% |
| **DOGE** | 0.0841 | 0.25 | -66.9% |
| **ATOM** | 1.055 | 4.19 | -74.8% |
| **XRP** | 1.066 | 2.84 | -62.4% |
| **BNB** | 782.00 | 1,279.68 | -38.9% |
| **ADA** | 0.2675 | 0.82 | -67.5% |
| **DOT** | 0.696 | 4.29 | -83.8% |
| **LINK** | 7.87 | 22.78 | -65.5% |
| **LTC** | 50.00 | 135.90 | -63.2% |
| **BCH** | 461.92 | 601.35 | -23.2% |
| **FIL** | 0.32 | 2.45 | -86.9% |
| **UNI** | 2.00 | 8.60 | -76.7% |
| **AVAX** | 6.02 | 28.63 | -79.0% |
| **ETC** | 4.743 | 20.61 | -77.0% |
| **TRX** | 0.3005 | 0.34 | -10.9% |
| **XLM** | 0.1651 | 0.39 | -57.2% |

---

## Conclusion

During the October 10, 2025 incident:

1. **Spot prices** for altcoins on Binance were severely depressed compared to US-regulated exchanges. ATOM's minimum price of **$0.001** represents a **99.98% drop** from its normal value.

2. **Coin-Margined Futures** also experienced significant price drops, with some assets like FIL dropping **86.9%** and DOT dropping **83.8%**.

## Source Data

Analysis scripts and raw data files available in: `analysis/spot/`

- `compare_all_exchanges.py` - Main comparison script
- `download_coin_margined.py` - Coin-margined futures download script
- Individual coin folders with download scripts and CSV data
