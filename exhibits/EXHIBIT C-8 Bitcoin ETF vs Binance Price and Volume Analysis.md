# EXHIBIT C-8: Bitcoin ETF vs Binance Price & Volume Analysis

## Overview

Comparative analysis of Bitcoin ETF (IBIT, FBTC) performance vs Binance spot market during the October 10, 2025 incident, including volatility patterns, anomaly detection, and trading volume comparisons.

---

## 1. ETF Price Analysis Results

### 1.1 IBIT (iShares Bitcoin Trust) Analysis

**Full Period Data Analysis**
- **Data Points**: 11,825 data points analyzed
- **Time Range**: 2025-10-01 08:00:00 to 2025-12-30 23:55:00
- **Conversion Ratio**: 1759.43 (Binance / IBIT, based on US morning 09:30-12:00 ET)

**Volatility Analysis**
- **Global Volatility Multiplier** (15-min window, 9,569 samples):
  - Average: 0.96x (Binance volatility typically 96% of IBIT)
  - Median: 0.96x

**Historical Anomaly Detection**
(15m & 1h windows | Binance Vol > 1% & Magnitude > 1.5x IBIT)

Found **3 significant independent events**:

| Time Window | Timestamp | Binance Change | IBIT Change | Multiplier | Type |
|-------------|-----------|----------------|-------------|------------|------|
| 15m | 2025-10-10 21:15:00 | -9.33% | -5.04% | 1.8x | Drop |
| 1h | 2025-10-10 21:15:00 | -11.20% | -6.98% | 1.6x | Drop |
| 1h | 2025-10-10 23:40:00 | +1.23% | +0.70% | 1.8x | Pump |

**Price Drop Comparison**
- **IBIT Max Drop**: -29.38% (64.8 → 45.76 @ 2025-11-21 12:25:00)
- **Binance Max Drop**: -29.55% (114,425.7 → 80,616.26 @ 2025-11-21 12:25:00)

**October 10, 2025 Incident Analysis** (20:30:00 - 22:30:00 UTC)
- **IBIT Max Drop**: -7.97% (66.27 → 60.99 @ 21:25:00)
- **Binance Max Drop**: -12.78% (116,799.19 → 101,877.69 @ 21:20:00)
- **Theoretical Binance Low** (based on morning ratio): $107,307.57
- **Actual Binance Low**: $101,877.69
- **Deviation**: -$5,429.88 (-5.06% below expected)

---

### 1.2 FBTC (Fidelity Bitcoin Trust) Analysis

**Full Period Data Analysis**
- **Data Points**: 8,675 data points analyzed
- **Time Range**: 2025-10-01 08:20:00 to 2025-12-30 23:10:00
- **Conversion Ratio**: 1145.47 (Binance / FBTC, based on US morning 09:30-12:00 ET)

**Volatility Analysis**
- **Global Volatility Multiplier** (15-min window, 7,507 samples):
  - Average: 0.97x (Binance volatility typically 97% of FBTC)
  - Median: 0.96x

**Historical Anomaly Detection**
(15m & 1h windows | Binance Vol > 1% & Magnitude > 1.5x FBTC)

Found **5 significant independent events**:

| Time Window | Timestamp | Binance Change | FBTC Change | Multiplier | Type |
|-------------|-----------|----------------|-------------|------------|------|
| 15m | 2025-10-10 21:15:00 | -9.33% | -5.71% | 1.6x | Drop |
| 15m | 2025-12-18 13:45:00 | +1.11% | +0.70% | 1.6x | Pump |
| 1h | 2025-10-10 21:15:00 | -11.11% | -7.20% | 1.5x | Drop |
| 1h | 2025-10-10 23:35:00 | +1.45% | +0.95% | 1.5x | Pump |
| 1h | 2025-11-04 21:55:00 | -1.08% | -0.61% | 1.8x | Drop |

**Price Drop Comparison**
- **FBTC Max Drop**: -29.82% (100.16 → 70.29 @ 2025-11-21 12:25:00)
- **Binance Max Drop**: -29.65% (114,590.0 → 80,616.26 @ 2025-11-21 12:25:00)

**October 10, 2025 Incident Analysis** (20:30:00 - 22:30:00 UTC)
- **FBTC Max Drop**: -8.57% (101.84 → 93.11 @ 21:25:00)
- **Binance Max Drop**: -12.78% (116,799.19 → 101,877.69 @ 21:20:00)
- **Theoretical Binance Low** (based on morning ratio): $106,654.88
- **Actual Binance Low**: $101,877.69
- **Deviation**: -$4,777.19 (-4.48% below expected)

---

## 2. Trading Volume Comparison

### 2.1 Daily Trading Volume: Binance BTC vs IBIT

| Date | Binance Open | IBIT Open | Ratio (BTC/Share) | Binance Vol (BTC) | IBIT Vol (Equiv BTC) | Binance/IBIT |
|------|--------------|-----------|-------------------|-------------------|----------------------|--------------|
| 2025-10-01 | $117,381.65 | $66.30 | 0.00056482 | 5,722.61 | 32,637.42 | 0.18x |
| 2025-10-02 | $119,425.50 | $67.76 | 0.00056738 | 6,687.46 | 35,320.86 | 0.19x |
| 2025-10-03 | $122,509.00 | $68.61 | 0.00056000 | 5,790.67 | 46,616.67 | 0.12x |
| 2025-10-06 | $125,653.57 | $71.01 | 0.00056513 | 6,873.80 | 38,867.83 | 0.18x |
| 2025-10-07 | $121,295.55 | $70.97 | 0.00058510 | 6,174.85 | 47,791.08 | 0.13x |
| 2025-10-08 | $123,792.36 | $69.58 | 0.00056207 | 4,600.67 | 30,489.83 | 0.15x |
| 2025-10-09 | $120,259.08 | $70.15 | 0.00058332 | 5,683.53 | 32,524.73 | 0.17x |

**Average Volume Ratio**: ~0.16x (Binance volume approximately 16% of IBIT volume equivalent)

---

### 2.2 Bitcoin Holdings Comparison

**IBIT (iShares Bitcoin Trust ETF)**
- Holdings as of December 31, 2025: **770,791.55 BTC**
- Source: [BlackRock - iShares Bitcoin Trust ETF](https://www.blackrock.com/us/individual/products/333011/ishares-bitcoin-trust)

**Binance**
- Holdings as of January 1, 2026: **636,535.25 BTC**
- Source: [Binance Proof of Reserves](https://www.binance.com/en/proof-of-reserves)

---

## 3. Key Findings

### 3.1 Volatility Patterns
- Under normal conditions, Binance volatility tracks ETF volatility closely (~0.96-0.97x multiplier)
- October 10, 2025 incident shows **1.6-1.8x anomalous volatility amplification** on Binance

### 3.2 Price Deviations
- **IBIT**: Binance dropped 5.06% below theoretical price during incident
- **FBTC**: Binance dropped 4.48% below theoretical price during incident
- ETF prices maintained stability while Binance experienced extreme downward pressure

### 3.3 Market Dominance
- IBIT trading volume significantly exceeds Binance spot BTC volume (6.25x average)
- IBIT holds more BTC than Binance (770k vs 636k BTC)

---

## Source Data

Analysis scripts and raw data files available in:
- `analysis/etf/` - ETF comparison scripts and data
- `analysis/trading volume overview/` - Volume analysis scripts
