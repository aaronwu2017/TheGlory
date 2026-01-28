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

### Combined Spot and Coin-Margined Futures Minimum Prices

**Note:** "Diff %" represents the percentage drop compared to the Coinbase Minimum price (Reference).

| Coin | Coinbase Min (Ref) | Binance Spot Min (Diff%) | Binance COIN-M Min (Diff%) | Gemini Spot Min (Diff%) |
|------|--------------------|--------------------------|----------------------------|-------------------------|
| **BTC** | 107,000.00 | 102,000.00 (-4.7%) | 101,389.70 (-5.2%) | 107,000.00 (0.0%) |
| **SOL** | 176.85 | 168.79 (-4.6%) | 137.21 (-22.4%) | 172.10 (-2.7%) |
| **DOGE** | 0.1500 | 0.0950 (-36.7%) | 0.0841 (-43.9%) | 0.1819 (+21.3%) |
| **AAVE** | 128.00 | 79.51 (-37.9%) | 63.42 (-50.5%) | 178.34 (+39.3%) |
| **ATOM** | 3.000 | **0.001 (-99.9%)** | 1.055 (-64.8%) | 3.000 (0.0%) |
| **WIF** | 0.3200 | 0.0620 (-80.6%) | 0.1252 (-60.9%) | 0.1454 (-54.6%) |
| **WLD** | 0.880 | 0.264 (-70.0%) | 0.2484 (-71.8%) | - |
| **POL** | - | 0.1152 | - | 0.20 |
| **SKY** | 0.03489 | 0.03491 (+0.1%) | - | 0.05411 (+55.1%) |
| **PEPE** | 0.000005 | 0.000003 (-40.0%) | - | 0.000006 (+20.0%) |
| **BONK** | 0.000013 | 0.000004 (-69.2%) | - | 0.000007 (-46.2%) |
| **ENA** | 0.282 | 0.1313 (-53.4%) | - | - |
| **CRV** | 0.489 | 0.1805 (-63.1%) | - | 0.460 (-5.9%) |
| **ETH** | 3,510.00 | 3,435.00 (-2.1%) | 3,378.19 (-3.8%) | 3,681.00 (+4.9%) |
| **XRP** | 1.771 | 1.2543 (-29.2%) | 1.066 (-39.8%) | 2.100 (+18.6%) |
| **ADA** | 0.6177 | 0.2737 (-55.7%) | 0.2675 (-56.7%) | - |
| **DOT** | 2.860 | 0.633 (-77.9%) | 0.696 (-75.7%) | 2.867 (+0.2%) |
| **LINK** | 15.00 | 7.90 (-47.3%) | 7.87 (-47.5%) | 16.00 (+6.7%) |
| **LTC** | 71.73 | 52.71 (-26.5%) | 50.00 (-30.3%) | 104.50 (+45.7%) |
| **BCH** | 474.48 | 482.00 (+1.6%) | 461.92 (-2.6%) | 500.05 (+5.4%) |
| **FIL** | 1.743 | 0.320 (-81.6%) | 0.320 (-81.6%) | 1.0001 (-42.6%) |
| **UNI** | 5.00 | 2.00 (-60.0%) | 2.00 (-60.0%) | 4.95 (-1.0%) |
| **AVAX** | 17.00 | 8.52 (-49.9%) | 6.02 (-64.6%) | 20.88 (+22.8%) |
| **ETC** | 11.94 | 7.00 (-41.4%) | 4.743 (-60.3%) | - |
| **XLM** | 0.280 | 0.160 (-42.9%) | 0.1651 (-41.0%) | - |

---

## Conclusion

During the October 10, 2025 incident:

1. **Spot prices** for altcoins on Binance were severely depressed compared to US-regulated exchanges. ATOM's minimum price of **$0.001** represents a **99.98% drop** from its normal value.

2. **Coin-Margined Futures** also experienced significant price drops, with some assets like AAVE even trading **20.2%** below Binance Spot.

## Source Data

Analysis scripts and raw data files available in: `analysis/spot/`

- `compare_all_exchanges.py` - Main comparison script
- `download_coin_margined.py` - Coin-margined futures download script
- Individual coin folders with download scripts and CSV data
