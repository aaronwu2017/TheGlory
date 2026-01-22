# EXHIBIT C-11: Buy-Side Liquidity Threshold Summary (20:50–21:50 UTC)

**Time window analyzed:** 20:50–21:50 UTC on 2025-10-10

**Method:** Computed total bid-side liquidity across 25 levels for each snapshot; counted snapshots where bid liquidity < $10,000 within the window. Results produced by `analysis/liquidity-orderbook-viewer/analyze_liquidity_threshold_window.py`.

## Snapshot Results (20:50–21:50 UTC)

- binance-futures_book_snapshot_25_2025-10-10_BTCUSDC
  - Snapshots: 68,548
  - Below $10,000: 394 (0.57%)
  - Avg bid: $409,349 | Min: $5,740 | Max: $10,292,761
- binance-futures_book_snapshot_25_2025-10-10_BTCUSDT
  - Snapshots: 70,121
  - Below $10,000: 740 (1.06%)
  - Avg bid: $1,265,032 | Min: $2,934 | Max: $108,456,804
- bitget-futures_book_snapshot_25_2025-10-10_BTCUSDT
  - Snapshots: 35,960
  - Below $10,000: 289 (0.80%)
  - Avg bid: $1,715,334 | Min: $345 | Max: $12,105,359
- bybit_book_snapshot_25_2025-10-10_BTCPERP
  - Snapshots: 150,807
  - Below $10,000: 2 (0.00%)
  - Avg bid: $1,245,404 | Min: $8,951 | Max: $6,155,755
- coinbase-international_book_snapshot_25_2025-10-10_BTC-PERP
  - Snapshots: 482,840
  - Below $10,000: 1 (0.00%)
  - Avg bid: $1,341,628 | Min: $23 | Max: $14,140,348
- huobi-dm-linear-swap_book_snapshot_25_2025-10-10_BTC-USDT
  - Snapshots: 119,175
  - Below $10,000: 0 (0.00%)
  - Avg bid: $792,164,526 | Min: $6,199,287 | Max: $12,741,447,096
- hyperliquid_book_snapshot_25_2025-10-10_BTC
  - Snapshots: 6,265
  - Below $10,000: 26 (0.42%)
  - Avg bid: $6,444,324 | Min: $240 | Max: $154,115,605
- kucoin-futures_book_snapshot_25_2025-10-10_XBTUSDCM
  - Snapshots: 791,640
  - Below $10,000: 0 (0.00%)
  - Avg bid: $1,598,199,417 | Min: $6,517,300 | Max: $16,136,354,038
- okex-swap_book_snapshot_25_2025-10-10_BTC-USDC-SWAP
  - Snapshots: 265,705
  - Below $10,000: 0 (0.00%)
  - Avg bid: $823,892,242 | Min: $7,677,224 | Max: $21,970,908,837
- okex-swap_book_snapshot_25_2025-10-10_BTC-USDT-SWAP
  - Snapshots: 349,720
  - Below $10,000: 0 (0.00%)
  - Avg bid: $37,334,551 | Min: $76,400 | Max: $1,572,782,345

## Notes
- Window set to 20:50–21:50 UTC to encompass late unified account liquidations (reports indicate activity continued past ~21:40 UTC). Adjustable via `START_TIME`/`END_TIME` in the script.
- Figures are as reported by the script output; no further smoothing or filtering applied.
