# Binance System Outage Claim Calculation Report

## Event Overview

- **Event Date**: October 10, 2025
- **Outage Start Time**: 16:40:38 UTC
- **Liquidation Completion Time**: 21:19:53 UTC
- **Final Account Balance**: 0 (Full Liquidation)

---

## 🎯 Total Claim Amount: 18,999.08 USDT

---

## Part 1: Position Analysis at 16:40 (Before Outage)

### Column Definitions

| Term | Formula | Description |
|------|---------|-------------|
| **Entry->Mark** | (Mark Price - Entry Price) × Qty | Unrealized PnL at 16:40 (Existing floating loss before outage) |
| **Mark->Liq** | (Liq Price - Mark Price) × Qty | Loss incurred **DURING** the outage period |
| **Entry->Liq** | Entry->Mark + Mark->Liq | Total Realized PnL |

> Note: Formula signs are reversed for SHORT positions.

### Detailed PnL Breakdown by Symbol

| Symbol | Side | Qty | Entry | Mark@16:40 | Liq Price | Entry->Mark | Mark->Liq | Entry->Liq |
|--------|------|-----|-------|------------|-----------|-------------|-----------|------------|
| 1000BONKUSDC | LONG | 150,000 | 0.022895 | 0.018111 | 0.009021 | -717.62 | -1,363.43 | -2,081.05 |
| 1000PEPEUSDC | LONG | 1,500,000 | 0.009996 | 0.008868 | 0.004373 | -1,691.64 | -6,743.31 | -8,434.95 |
| BBUSDT | LONG | 200,000 | 0.172595 | 0.158578 | 0.091180 | -2,803.43 | -453.17 | -3,256.60 |
| BTCUSDC | SHORT | 0.50 | 119,558.60 | 119,186.98 | 118,138.00 | +185.81 | +524.49 | +710.30 |
| BTCUSDT | SHORT | 0.50 | 106,212.73 | 119,121.40 | 106,088.00 | -6,454.34 | +6,516.70 | +62.36 |
| CRVUSDT | LONG | 5,000 | 0.784400 | 0.706149 | 0.307000 | -391.26 | -1,995.74 | -2,387.00 |
| ENAUSDC | LONG | 13,000 | 0.645038 | 0.527342 | 0.205600 | -1,530.05 | -4,182.65 | -5,712.70 |
| ETHUSDC | SHORT | 1.00 | 4,360.56 | 4,125.41 | 3,998.00 | +235.15 | +127.41 | +362.56 |
| SKYUSDT | LONG | 200,000 | 0.065250 | 0.065737 | 0.047666 | +97.45 | -3,614.33 | -3,516.88 |
| STBLUSDT | LONG | 20,000 | 0.158960 | 0.175508 | 0.122100 | +330.95 | -1,068.15 | -737.20 |
| WIFUSDC | LONG | 5,000 | 0.766600 | 0.685381 | 0.312000 | -406.09 | -1,866.91 | -2,273.00 |
| WIFUSDT | LONG | 2,000 | 0.842050 | 0.685159 | 0.275600 | -313.78 | -819.12 | -1,132.90 |
| WLDUSDC | LONG | 3,000 | 1.316133 | 1.200181 | 0.359000 | -347.86 | -2,523.54 | -2,871.40 |
| **TOTAL** | | | | | | **-13,806.70** | **-17,461.75** | **-31,268.45** |

### Loss Component Summary

| Component | Amount (USDT) | Description |
|-----------|---------------|-------------|
| Entry->Mark (Unrealized@16:40) | -13,806.70 | Floating loss existing before outage |
| Mark->Liq (Loss DURING Outage) | -17,461.75 | **Losses caused by inability to operate** |
| Entry->Liq (Total Realized Loss) | -31,268.45 | Total realized loss |

---

## Part 2: Account Changes (16:40 - 21:19)

### 2.1 Realized PnL

| Asset | Amount |
|-------|--------|
| USDT | -11,304.21 |
| USDC | -21,345.44 |
| **Total** | **-32,649.65** |

### 2.2 Transfer Details (Rescue Funds)

| Time (UTC) | Amount (USDT) | Type |
|------------|---------------|------|
| 2025-10-10 21:00:04 | +2,500.00 | IN |
| 2025-10-10 21:00:31 | +1,800.00 | IN |
| 2025-10-10 21:00:54 | +1,000.00 | IN |
| 2025-10-10 21:01:52 | +800.00 | IN |
| 2025-10-10 21:05:01 | -2,000.00 | OUT |
| 2025-10-10 21:15:15 | +2,000.00 | IN |
| 2025-10-10 21:16:31 | +6,856.82 | IN |

| Summary | Amount |
|---------|--------|
| Total In | +14,956.82 |
| Total Out | -2,000.00 |
| **Net Transfer** | **+12,956.82** |

### 2.3 Fees

| Asset | Amount |
|-------|--------|
| USDT | -155.78 |
| USDC | -0.35 |
| **Total** | **-156.13** |

---

## Part 3: Positions Opened After 16:40 (Invalid Operations)

These positions were opened during the system outage period. Due to the inability to operate normally, they resulted in losses.

| Symbol | Side | Entry | Close | Realized PnL |
|--------|------|-------|-------|--------------|
| YGGUSDT | LONG | 0.1560 | 0.1392 | -336.00 |
| DOGEUSDC | LONG | 0.2326 | 0.1281 | -1,045.20 |
| **Total** | | | | **-1,381.20** |

---

## Part 4: Account Equity Calculation at 16:40

### 4.1 Method 1: Reverse from Realized PnL

**Principle**: Balance after liquidation = 0, so Balance@16:40 + Changes = 0

```
Realized PnL:        -32,649.65
Net Transfer:        +12,956.82
Fees:                   -156.13
─────────────────────────────────
Total Change:        -19,848.96
───────────────────────────────── 
∴ Wallet Balance@16:40: +19,848.96
```

### 4.2 Account Equity Calculation

**Principle**: Account Equity = Wallet Balance + Unrealized PnL

```
Wallet Balance (16:40):    +19,848.96
Unrealized PnL (16:40):    -13,806.70
─────────────────────────────────────
∴ Account Equity (16:40):   +6,042.26
```

### 4.3 Verification: Balance Equation

**Check**: Final Balance = Equity@16:40 + All Changes During Outage

```
Account Equity (16:40):    +6,042.26
Loss During Outage:       -17,461.75
New Position Loss:         -1,381.20
Net Transfer:             +12,956.82
Fees:                        -156.13
─────────────────────────────────────
Calculated Final Balance:      -0.00
Actual Final Balance:           0.00

✅ VERIFIED!
```

---

## Part 5: Final Conclusion

### Account Status at 16:40 (Before Outage)

| Item | Amount (USDT) |
|------|---------------|
| Wallet Balance | +19,848.96 |
| Unrealized PnL | -13,806.70 |
| **Account Equity** | **+6,042.26** |

### Loss Breakdown

| Loss Type | Amount (USDT) | Claimable? |
|-----------|---------------|------------|
| Pre-existing Floating Loss (Entry->Mark) | -13,806.70 | ❌ No |
| **Outage Loss (Mark->Liq)** | **-17,461.75** | ✅ **YES** |
| **New Position Loss (After 16:40)** | **-1,381.20** | ✅ **YES** |
| Net Transfer In | +12,956.82 | - |
| Final Balance | 0.00 | - |

---

## Part 6: HKIAC Arbitration Claim Calculation

### Claim Methodology

Your claim is for the **total value lost due to the Binance system outage** on October 10, 2025. There are two equivalent methods to calculate this amount:

- **Method 1**: Account Value + Capital Injected = Account Equity@16:40 + Net Transfer
- **Method 2**: Sum of Losses = Mark->Liq Loss + New Position Loss + Fees

Both methods yield the SAME result.

---

### Method 1: Account Value + Capital Injected

| Item | Amount (USDT) | Description |
|------|---------------|-------------|
| **A. Account Equity at 16:40** | +6,042.26 | Value you held before the outage |
| | | = +19,848.96 (Balance) + (-13,806.70) (Unalized PnL) |
| **B. Net Transfer Amount** | +12,956.82 | Capital injected trying to save positions |
| | | In: +14,956.82, Out: -2,000.00 |
| **TOTAL CLAIM (A + B)** | **+18,999.08** | |

---

### Method 2: Sum of All Losses

| Item | Amount (USDT) | Description |
|------|---------------|-------------|
| **C. Mark->Liq Loss** | +17,461.75 | Loss on held positions during outage |
| **D. New Position Loss** | +1,381.20 | Loss on positions opened after 16:40 |
| **E. Fees** | +156.13 | Transaction fees |
| **TOTAL CLAIM (C + D + E)** | **+18,999.08** | |

---

### Verification

```
Method 1: 6,042.26 + 12,956.82 = 18,999.08
Method 2: 17,461.75 + 1,381.20 + 156.13 = 18,999.08

✅ Both methods match!
```

---

## 🎯 TOTAL CLAIM AMOUNT: 18,999.08 USDT

---

## Reconciliation Notes

### Why are the two methods equivalent?

**Method 1** calculates: What you had before the outage + What you put in during the outage.
**Method 2** calculates: Where the money went (Losses).

Since the final balance is 0, these two amounts must be equal:
`Initial Equity + Injections = Total Losses`

### Why is "Entry->Mark" loss not claimed?

The "Entry->Mark" loss (-13,806.70) represents unrealized losses that already existed at 16:40:38 UTC, before the system outage began. These are considered normal market risks and are not attributable to the system failure, hence they are excluded from the claim.

### Realized PnL Reconciliation

```
Part 1 (Held Positions):     -31,268.45
Part 3 (New Positions):       -1,381.20
───────────────────────────────────────
Total Position PnL:          -32,649.65
Transaction History PnL:     -32,649.65

✅ Perfectly matched!
```

---

## Data Sources

| Data Type | Filename |
|-----------|----------|
| Position History | `0627553e-e93b-11f0-9062-0e3291b69067-1.csv` |
| Transaction History | `f2c71b64-e93a-11f0-a536-06a0ac25cdaf-1.csv` |
| Trade History | `f0c7b84c-e93a-11f0-bfa4-06a0ac25cdaf-1.csv` |
| Mark Price | Binance API (data.binance.vision) |

---

## Running the Calculation Script

To generate the full detailed report in your terminal:

```bash
python complete_loss_report.py
```

---

**Report Generated On**: January 25, 2025
