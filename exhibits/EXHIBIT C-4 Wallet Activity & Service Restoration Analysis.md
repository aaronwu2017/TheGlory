# EXHIBIT C-4: Wallet Activity & Service Restoration Analysis

## Overview

The cryptocurrency withdrawal halt was caused by Binance's internal technical failure, not blockchain congestion. On-chain data confirms that both Bitcoin and Ethereum networks remained fully operational and capable of processing transactions during the relevant period.

---

## Network Status Analysis

### 1. Bitcoin Network (BTC): Fully Operational

**Reference**: [Mempool.space - Block 918505](https://mempool.space/block/00000000000000000001a54602824c4c5c1020ad423a12d9ce523fb52dee3d16)

**Evidence**: 
- Network data shows normal satoshis per vByte (sats/vB) levels
- Blockchain continued processing transactions normally
- No network congestion or capacity issues

### 2. Ethereum Network (ETH): High Fees, But Fully Functional

**During Crash (Block #23549966)**: [Etherscan Link](https://etherscan.io/block/23549966)
- Gas fees elevated above typical levels but within acceptable operational range
- Network continued processing transactions normally

**Post-Crash (Block #23549999)**: [Etherscan Link](https://etherscan.io/block/23549999)
- Gas fees spiked to 400 Gwei
- Blockchain continued processing transactions normally. Similar fee levels occurred during market peaks in 2021-2022

---

## Conclusion

The halt in Binance's cryptocurrency withdrawal services was **not** due to blockchain network constraints. Both Bitcoin and Ethereum networks demonstrated normal operational capacity throughout the incident period, indicating that the service disruption was attributable to **Binance's internal systems and infrastructure failures**.

---

## Wallet Activity Data

### High-Volume Wallet Transfers During Incident Period

| Wallet Address | Type | Transfer Frequency | Last Successful Transfer (UTC) | Service Restoration (UTC) |
|---|---|---|---|---| 
| [0x28C6c06298d514Db089934071355E5743bf21d60](https://intel.arkm.com/explorer/address/0x28C6c06298d514Db089934071355E5743bf21d60) | Hot Wallet | Multiple times per minute | [2025-10-10 21:12:11](https://intel.arkm.com/explorer/tx/0xda4a5e7c91a38bc57e2d2df131519b73a45505a0c735cdbca8c0a6b3596c9de6) | [2025-10-10 22:19:35](https://intel.arkm.com/explorer/tx/0xf6b13b7618ac2f75d8eb60d4244459c28bb79c7e493dcb79459686ef5c3d4e0f) |
| [0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549](https://intel.arkm.com/explorer/address/0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549) | Hot Wallet | Multiple times per minute | [2025-10-10 21:11:59](https://intel.arkm.com/explorer/tx/0x8ea2412342da66a22d651d64c1db2c0937d2a0670b54d8994517e9167e7fe024) | [2025-10-10 22:19:35](https://intel.arkm.com/explorer/tx/0xcf5831c1516437c81c7a4bfab81bcd605ab6e6ac85e6caa732dacead06d48b5d) |
| [bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h](https://intel.arkm.com/explorer/address/bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h) | Bitcoin Hot Wallet | See detailed analysis below | 2025-10-10 20:52:26 | 2025-10-10 21:42:47 |

### Bitcoin Wallet [bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h](https://intel.arkm.com/explorer/address/bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h) Outflow Activity Pattern

- **Total Time Points Analyzed**: 91 (excluding intervals < 1 minute)
- **Median Transfer Interval**: 9 minutes 17 seconds (00:09:17)
- **Mean Transfer Interval**: Approximately 11 minutes 8 seconds (00:11:08)

**Interpretation**: transfers resumed at regular intervals following service restoration at 22:19:35 UTC, confirming operational recovery.

### Outflow Timestamps (UTC)

```
04:09:54  07:23:13  11:50:04  16:00:44
04:11:20  07:58:52  11:52:29  16:06:17
04:15:29  08:03:31  11:54:07  16:09:59
04:20:24  08:12:52  12:13:36  16:21:15
04:25:05  08:23:44  12:20:57  16:34:37
04:34:11  08:25:47  12:36:22  16:52:29
04:45:53  08:31:34  12:39:19  16:56:40
04:52:28  08:31:51  12:44:14  17:32:52
05:09:50  08:40:26  12:48:19  17:44:41
05:40:42  09:03:40  13:00:02  18:14:42
05:52:13  09:10:00  13:19:39  18:32:30
05:54:45  09:33:10  13:31:38  18:35:24
05:58:22  10:02:54  13:47:11  19:01:45
05:59:53  10:06:06  14:00:29  19:05:59
06:12:15  10:13:42  14:26:29  19:20:48
06:20:39  10:49:13  14:39:03  19:28:13
06:22:12  10:55:19  14:44:53  19:52:33
06:31:29  10:56:58  14:55:59  20:14:11
06:50:45  10:59:51  15:05:16  20:28:50
07:07:04  11:10:52  15:07:03  20:41:02
07:10:09  11:22:17  15:18:36  20:51:13
07:15:48  11:25:56  15:53:09  20:52:26
07:20:07  11:38:12  15:57:11
```

---

## Institutional Market Maker Context






## 5. Institutional Market Maker Context

**Wintermute** is recognized as a dominant global market maker and, based on information and belief, is responsible for maintaining liquidity for digital assets including SUI, ATOM, and BTC on the Respondent's platform.

### Evidence of Infrastructure Failure Preventing Liquidity Provision
On-chain evidence (see: [transaction](https://intel.arkm.com/explorer/tx/e44c8dad4b2a8a68c5eaaf6ec5e5662c8b3e9b2a8d1ffdc45e6ad13c4408b35f)) confirms that Wintermute successfully executed a withdrawal of 203.10938323 BTC immediately following service recovery. This substantial capital movement demonstrates that the market maker remained operationally responsive. Consequently, the complete lack of liquidity for BTC, SUI, ATOM, and other digital assets during the outage cannot be attributed to a failure by the market maker to discharge its bilateral quoting obligations, but rather points to a platform-side failure by Binance that prevented willing market makers from accessing the order book.

Evgeny Gaevoy, CEO of Wintermute, publicly confirmed that the lack of market depth during the crash was a direct result of exchange infrastructure failure (inability to move inventory), not market maker discretion.

> "Generally, what happens when the market crashes is things just stop working everywhere. Especially as a market maker, basically what you end up doing is... let's say you buy on Binance, sell on Coinbase. You end up having pretty big stablecoin inventory on Coinbase, you end up having all kinds of tokens on Binance, but you cannot move them over because for both of them, basically all the withdrawals will be completely flooded. It will be impossible to move things over.
>
> So when people are saying 'market makers went out of the market because they were scared of the conditions or didn't want to provide liquidity,' most of the time we simply couldn't. Because **we couldn't [show] bids in one place, we couldn't show offers in the other place because we just couldn't move inventory around.**"

* **Source:** *Wintermute CEO breaks down crypto's record breaking $20B+ liquidation event* (Interview with The Block)
* **Timestamp:** [04:52 - 05:35](https://youtu.be/LPQGl6Ju16U?t=292)

**Conclusion:** There is no definitive evidence of widespread system outages outside of Binance; other platforms are merely experiencing Ethereum network congestion, not a complete halt. The complete lack of liquidity for BTC, SUI, ATOM, and other digital assets during the outage cannot be attributed to a failure by the market maker to discharge its bilateral quoting obligations. Rather, the evidence points to a **platform-side failure by the Respondent** that prevented willing and able market makers from accessing the order book and managing inventory. 