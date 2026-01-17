# ETF Analysis Results

## IBIT Analysis

```
--- Loading Binance Data ---
Binance Path: data\binance data
Found 90 ZIP files in Binance directory.

==================== IBIT Analysis ====================
--- Processing IBIT Data ---
IBIT Path: data\BATS_IBIT, 5_unix.csv
Original data rows: IBIT = 14144, Binance = 25920

==================== Full Data Analysis (IBIT) ====================
Analyzing 11825 data points for IBIT vs Binance...
Data Time Range: 2025-10-01 08:00:00 to 2025-12-30 23:55:00
----------------------------------------
Advanced Analysis (IBIT vs Binance):
Global Volatility Multiplier (15-min window, samples=9569):
  -> Avg Multiplier: 0.96x (Binance volatility is usually 0.96x of IBIT)
  -> Median Multiplier: 0.96x
----------------------------------------
>>> Historical Anomaly Scan (15m & 1h | Binance Vol > 1% & Mag > 1.5x IBIT) <<<
Found 3 significant independent events:
[15m] 2025-10-10 21:15:00  Binance: -9.33% vs IBIT: -5.04% (倍数:1.8x) - Drop
[1h] 2025-10-10 21:15:00  Binance:-11.20% vs IBIT: -6.98% (倍数:1.6x) - Drop
[1h] 2025-10-10 23:40:00  Binance:  1.23% vs IBIT:  0.70% (倍数:1.8x) - Pump
----------------------------------------
Interval Price Change Analysis (Based on Low):
IBIT    Max Drop: -29.38% (Start: 64.8 -> Low: 45.76 @ 2025-11-21 12:25:00)
Binance Max Drop: -29.55% (Start: 114425.7 -> Low: 80616.25627536 @ 2025-11-21 12:25:00)
----------------------------------------
Theoretical Price Analysis (Ref: US Morning 09:30:00 - 12:00:00 ET):
  -> Avg Conversion Ratio: 1759.4289 (Binance / IBIT)

==================== Specific Time Range Analysis (IBIT) ====================
Target Timestamp (Unix): 1760128200 -> 1760135400 (UTC: 2025-10-10 20:30:00 -> 2025-10-10 22:30:00)
Analyzing 25 data points for IBIT vs Binance...
Data Time Range: 2025-10-10 20:30:00 to 2025-10-10 22:30:00
Interval Price Change Analysis (Based on Low):
IBIT    Max Drop: -7.97% (Start: 66.27 -> Low: 60.99 @ 2025-10-10 21:25:00)
Binance Max Drop: -12.78% (Start: 116799.19219565 -> Low: 101877.68981743 @ 2025-10-10 21:20:00)
----------------------------------------
Theoretical Binance Low (based on morning ratio): 107307.57
Actual Binance Low: 101877.69 (Diff: -5429.88)
```

## FBTC Analysis

```
==================== FBTC Analysis ====================
--- Processing FBTC Data ---
FBTC Path: data\BATS_FBTC, 5.csv
Original data rows: FBTC = 14166, Binance = 25920

==================== Full Data Analysis (FBTC) ====================
Analyzing 8675 data points for FBTC vs Binance...
Data Time Range: 2025-10-01 08:20:00 to 2025-12-30 23:10:00
----------------------------------------
Advanced Analysis (FBTC vs Binance):
Global Volatility Multiplier (15-min window, samples=7507):
  -> Avg Multiplier: 0.97x (Binance volatility is usually 0.97x of FBTC)
  -> Median Multiplier: 0.96x
----------------------------------------
>>> Historical Anomaly Scan (15m & 1h | Binance Vol > 1% & Mag > 1.5x FBTC) <<<
Found 5 significant independent events:
[15m] 2025-10-10 21:15:00  Binance: -9.33% vs FBTC: -5.71% (倍数:1.6x) - Drop
[15m] 2025-12-18 13:45:00  Binance:  1.11% vs FBTC:  0.70% (倍数:1.6x) - Pump
[1h] 2025-10-10 21:15:00  Binance:-11.11% vs FBTC: -7.20% (倍数:1.5x) - Drop
[1h] 2025-10-10 23:35:00  Binance:  1.45% vs FBTC:  0.95% (倍数:1.5x) - Pump
[1h] 2025-11-04 21:55:00  Binance: -1.08% vs FBTC: -0.61% (倍数:1.8x) - Drop
----------------------------------------
Interval Price Change Analysis (Based on Low):
FBTC    Max Drop: -29.82% (Start: 100.16 -> Low: 70.29 @ 2025-11-21 12:25:00)
Binance Max Drop: -29.65% (Start: 114590.0 -> Low: 80616.25627536 @ 2025-11-21 12:25:00)
----------------------------------------
Theoretical Price Analysis (Ref: US Morning 09:30:00 - 12:00:00 ET):
  -> Avg Conversion Ratio: 1145.4718 (Binance / FBTC)

==================== Specific Time Range Analysis (FBTC) ====================
Target Timestamp (Unix): 1760128200 -> 1760135400 (UTC: 2025-10-10 20:30:00 -> 2025-10-10 22:30:00)
Analyzing 24 data points for FBTC vs Binance...
Data Time Range: 2025-10-10 20:30:00 to 2025-10-10 22:30:00
Interval Price Change Analysis (Based on Low):
FBTC    Max Drop: -8.57% (Start: 101.84 -> Low: 93.11 @ 2025-10-10 21:25:00)
Binance Max Drop: -12.78% (Start: 116799.19219565 -> Low: 101877.68981743 @ 2025-10-10 21:20:00)
----------------------------------------
Theoretical Binance Low (based on morning ratio): 106654.88
Actual Binance Low: 101877.69 (Diff: -4777.19)
```
