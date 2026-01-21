# EXHIBIT C-9: Mark Price Calculation Discrepancy Analysis

## Overview

Analysis of Binance's official Mark Price calculation formula reveals significant discrepancies when applied to publicly available order book data, suggesting potential manipulation or incorrect implementation during the October 10, 2025 incident.

---

## Binance's Official Mark Price Calculation Formula

**Source**: [Binance Support - How is the Mark Price for Perpetual Contract Calculated?](https://www.binance.info/en-ZA/support/faq/detail/360033525071)

### How to calculate the Mark Price for USDⓈ-M quarterly delivery contracts?

#### Before the delivery date:

```
Mark Price = Price Index + Moving Average (30 seconds basis)
```

Where:
- **Moving Average (30 seconds basis)** is calculated as:
  - Moving Average ((Bid1 + Ask1) / 2 - Price Index)
  - Calculated every second over a 30 seconds interval

#### On the delivery date:

**i) If the time to delivery is greater than 30 minutes**

Using BTCUSDT 0925 as an example:
```
Mark Price before 25 September 2020, 07:29:59 UTC
= Price Index + Moving Average (30 seconds basis)

Moving Average (30 Seconds Basis) 
= Moving Average ((Bid1 + Ask1) / 2 - Price Index), 
  calculated every second over a 30 seconds interval
```

**ii) If time to delivery is 30 minutes or less**

```
Mark Price on 25 September 2020, 07:30:00 - 07:59:59 UTC
= Average of the Price Index, 
  calculated every second between 07:30:00 and 07:59:59 UTC 
  on the delivery day
```

---

## Critical Discrepancy

### Problem Statement

When applying Binance's official Mark Price calculation formula to the publicly available order book depth data from Binance Public Data, the calculated Mark Price **does not match** the actual Mark Price used by Binance's system during the October 10, 2025 incident.

### Data Sources

1. **Formula Source**: Binance official documentation (linked above)
2. **Order Book Data**: Binance Public Data - Order Depth records
   - **Public Download**: [Binance Public Data - BTCUSDT Book Depth](https://data.binance.vision/?prefix=data/futures/um/daily/bookDepth/BTCUSDT/)

### How to Calculate Average Price at Each Level

The Binance book depth data contains:
- **notional**: The total notional value (in USD) at that price level
- **depth**: The amount of BTC (or contract size) at that price level

**Formula**:
```
Average Price at Level = notional / depth
```

#### Interpretation

- **Normal Market**: Bid price < Ask price
- **Anomaly**: Bid price > Ask price

#### Implication

This is a **clear and obvious system malfunction signal**. The presence of this anomaly provides Binance with sufficient time to:
1. Detect the system malfunction
2. Prepare circuit break mechanisms
3. Trigger protective measures to prevent further damage

The fact that such anomalies were present but circuit breaks were not activated raises serious questions about Binance's risk management protocols during the October 10, 2025 incident.

### BTCUSDT Order Book Data Sample

**Data Structure**: Each record contains:
- **timestamp**: Time of the snapshot
- **percentage**: Bid/Ask level (-5 to -1 for bids, 1 to 5 for asks)
- **depth**: Contract quantity at that level
- **notional**: Total USD value at that level
- **weighted_avg_price**: Calculated as notional / depth

**Sample Data from October 10, 2025, 21:21:33 UTC**:

| Timestamp | Percentage | Depth | Notional | Weighted Avg Price |
|---|---|---|---|---|
| 2025-10-10 21:21:33 | -5 | 117.374 | 12915218.8606 | 110034.750972106 |
| 2025-10-10 21:21:33 | -4 | 62.332 | 6989187.8815 | 112128.407262722 |
| 2025-10-10 21:21:33 | -3 | 17.817 | 2160477.0931 | 121259.308138295 |
| 2025-10-10 21:21:33 | -2 | 17.654 | 2142547.0931 | 121363.203724462 |
| 2025-10-10 21:21:33 | -1 | 17.654 | 2142547.0931 | 121363.265724482 |
| 2025-10-10 21:21:33 | 1 | 1235.76 | 134420963.8904 | 108775.946697093 |
| 2025-10-10 21:21:33 | 2 | 134.01 | 14636386.3867 | 109218.570544512 |
| 2025-10-10 21:21:33 | 3 | 1597.955 | 176158178.6736 | 110239.761866636 |
| 2025-10-10 21:21:33 | 4 | 1676.945 | 186366931.0854 | 110538.467919958 |
| 2025-10-10 21:21:33 | 5 | 1901.961 | 211847332.8178 | 111383.636582348 |

**Analysis**:
- **Bid Level -1**: Weighted Avg Price = 121,363.27
- **Ask Level 1**: Weighted Avg Price = 108,775.95

**Critical Observation**: Bid price (121,363.27) > Ask price (108,775.95)

This represents an **inverted order book** - a clear system malfunction that should have triggered immediate circuit breakers.

---

### Implications

The discrepancy between:
- **Expected Mark Price** (calculated using official formula + public order book data)
- **Actual Mark Price** (used for liquidations and ADL)





