# EXHIBIT C-10: Bitcoin Price Timeline Analysis

## 2025-10-10 Timeline

![Bitcoin Price Timeline - 2025-10-10](../analysis/timeline/Bitcoin_Price_Timeline_2025-10-10.png)

### Key Events on 2025-10-10

This timeline visualization shows the Bitcoin price movement on October 10, 2025, highlighting:

- **BTC Price** (solid blue line): Bitcoin price on Binance
- **IBIT Price** (dotted orange line): iShares Bitcoin Trust ETF price
- **Book Depth Anomaly** (red bars): Binance book depth anomaly indicator
- **Key Events**: 
  - [Trump Post about Tariff](https://truthsocial.com/@realDonaldTrump/115351840469973590)
  - Binance Crypto Withdrawals Halted
  - SPY Intraday Low
  - Binance Widespread System Overload Error

The visualization captures the binance BTC price dislocation from ibit and anomalies observed during this trading day.

---

## Bid Price Higher Than Ask Price Anomaly

### Overview
One of the critical anomalies detected on 2025-10-10 is the **book depth anomaly** where **bid price is higher than ask price**. This is a market manipulation indicator and is theoretically impossible in normal market conditions.

### Data Source & Methodology

**Source**: [Binance Vision - BTCUSDT Book Depth Data](https://data.binance.vision/?prefix=data/futures/um/daily/bookDepth/BTCUSDT/)

### How to Calculate Average Price at Each Level

The Binance book depth data contains:
- **notional**: The total notional value (in USD) at that price level
- **depth**: The amount of BTC (or contract size) at that price level

**Formula**:
```
Average Price at Level = notional / depth
```

### Interpretation

1. **Normal Market**: Bid price < Ask price 
2. **Anomaly**: Bid price > Ask price 
3. **Implication**: 
   - This is a clear and obvious system malfunction signal
   - The presence of this anomaly provides Binance with sufficient time to prepare
   - Once prepared, Binance can quickly trigger circuit break mechanisms to prevent further damage


