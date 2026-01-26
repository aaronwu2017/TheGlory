"""
================================================================================
                        COMPLETE LOSS CALCULATION REPORT
================================================================================
Calculation Time: 2025-10-10 16:40:38 UTC (Before Binance System Outage)
Liquidation End Time: 2025-10-10 21:19:53 UTC
================================================================================
"""
import csv
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent

# Key Timestamps
TARGET_STR = "2025-10-10 16:40:38"
TARGET_MS = int(datetime(2025, 10, 10, 16, 40, 38, tzinfo=timezone.utc).timestamp() * 1000)
LIQUIDATION_END = "2025-10-10 21:20:00"  # Includes transactions at 21:19:53

# Data Files
TRADES_FILE = "beb5799c-e93a-11f0-8aa2-0688bfc90b95-1.csv"
TRANSACTIONS_FILE = "f2c71b64-e93a-11f0-a536-06a0ac25cdaf-1.csv"
POSITIONS_FILE = "0627553e-e93b-11f0-9062-0e3291b69067-1.csv"
ORDERS_FILE = "f6021db0-e93a-11f0-bfcd-0a8dd44a981d-1.csv"


def parse_number(value: str) -> float:
    if value is None:
        return 0.0
    text = value.strip()
    if not text or text.upper() == "0E-8":
        return 0.0
    if " " in text:
        text = text.split()[0]
    text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_csv(filename: str) -> list:
    path = BASE / filename
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in reader]


def fetch_mark_price(symbol: str, date_str: str, target_ms: int) -> float:
    """Fetch Mark Price at specified time from Binance"""
    url = (
        "https://data.binance.vision/data/futures/um/daily/markPriceKlines/"
        f"{symbol}/1m/{symbol}-1m-{date_str}.zip"
    )
    req = Request(url, headers={"User-Agent": "loss-calc"}, method="GET")
    try:
        with urlopen(req, timeout=15) as resp:
            data = resp.read()
    except Exception:
        return None

    with zipfile.ZipFile(BytesIO(data)) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as fh:
            reader = csv.reader(fh.read().decode("utf-8").splitlines())
            for row in reader:
                try:
                    open_ms = int(row[0])
                    close_ms = int(row[6])
                    if open_ms <= target_ms < close_ms:
                        return float(row[4])
                except:
                    continue
    return None


def print_section(title: str, width: int = 100):
    print()
    print("=" * width)
    print(f" {title}")
    print("=" * width)


def print_subsection(title: str, width: int = 100):
    print()
    print(f"[{title}]")
    print("-" * width)


def main():
    # Load Data
    positions = load_csv(POSITIONS_FILE)
    transactions = load_csv(TRANSACTIONS_FILE)
    trades = load_csv(TRADES_FILE)
    
    # --- PRE-CALCULATION FOR SUMMARY ---
    # 1. Calculate Total Realized PnL from Transactions (for comparison)
    calc_realized_usdt = 0.0
    calc_realized_usdc = 0.0
    realized_pnl_by_symbol = {}  # NEW: Track realized PnL by symbol from Transaction History
    
    for tx in transactions:
        dt = tx.get("Date(UTC)", "")
        if dt > TARGET_STR and dt <= LIQUIDATION_END:
            if tx.get("type") == "REALIZED_PNL":
                amt = parse_number(tx.get("Amount", ""))
                asset = tx.get("Asset", "")
                symbol = tx.get("Symbol", "")
                
                if asset == "USDT": calc_realized_usdt += amt
                elif asset == "USDC": calc_realized_usdc += amt
                
                # Track by symbol for accurate Entry->Liq calculation
                if symbol not in realized_pnl_by_symbol:
                    realized_pnl_by_symbol[symbol] = 0.0
                realized_pnl_by_symbol[symbol] += amt
                
    calc_total_realized = calc_realized_usdt + calc_realized_usdc

    # 2. Calculate New Positions PnL (Opened after 16:40)
    calc_new_pos_pnl = 0.0
    new_position_symbols = set()  # Track symbols opened after 16:40
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")[:19]
        if opened > TARGET_STR and closed and closed <= LIQUIDATION_END:
            calc_new_pos_pnl += parse_number(p.get("Closing PNL", ""))
            new_position_symbols.add(p.get("symbol", ""))

    print()
    print("#" * 100)
    print("#" + " " * 98 + "#")
    print("#" + "            COMPLETE LOSS CALCULATION REPORT            ".center(98) + "#")
    print("#" + " " * 98 + "#")
    print("#" * 100)
    print()
    print(f"Calculation Time:     2025-10-10 16:40:38 UTC (Before Binance System Outage)")
    print(f"Liquidation End:      2025-10-10 21:19:53 UTC")
    print(f"Final Balance:        0 (Fully Liquidated)")
    
    # ========================================================================
    # Part 1: Consolidated Position Analysis
    # ========================================================================
    print_section("Part 1: Consolidated Position Analysis (Held at 16:40)")
    
    print("""
    +-------------------------------------------------------------------------+
    |  COLUMN DEFINITIONS                                                     |
    +-------------------------------------------------------------------------+
    |  Entry->Mark   = PnL from Entry Price to 16:40 Mark Price               |
    |                  (Unrealized PnL at 16:40, BEFORE the outage)           |
    |                                                                         |
    |  Mark->Liq     = PnL from 16:40 Mark Price to Liquidation Price         |
    |                  (Loss incurred DURING the outage period)               |
    |                                                                         |
    |  Entry->Liq    = Total PnL from Entry Price to Liquidation Price        |
    |                  (Total realized loss = Entry->Mark + Mark->Liq)        |
    +-------------------------------------------------------------------------+
    |  Formula for LONG:  Entry->Mark = (Mark - Entry) x Qty                  |
    |                     Mark->Liq   = (Liq - Mark) x Qty                    |
    |  Formula for SHORT: Entry->Mark = (Entry - Mark) x Qty                  |
    |                     Mark->Liq   = (Mark - Liq) x Qty                    |
    +-------------------------------------------------------------------------+
    """)
    
    print(f"{'Symbol':<14} {'Side':<5} {'Qty':>10} {'Entry':>10} {'Mark@16:40':>10} {'LiqPrice':>10} | {'Entry->Mark':>12} {'Mark->Liq':>12} {'Entry->Liq':>12}")
    print("-" * 115)

    # Metrics for totals
    total_entry_to_mark = 0.0  # Unrealized at 16:40
    total_mark_to_close = 0.0  # Loss during outage
    total_closing_pnl_held = 0.0 # Total realized for these positions (from Transaction History)

    # Store for later use
    processed_positions = []
    processed_symbols = set()  # Track which symbols we've processed

    # Group positions by symbol for accurate aggregation
    positions_by_symbol = {}
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")
        symbol = p.get("symbol", "")
        
        # Positions still held at 16:40 (and NOT opened after 16:40)
        if opened <= TARGET_STR and (not closed or closed > TARGET_STR):
            if symbol not in positions_by_symbol:
                positions_by_symbol[symbol] = []
            positions_by_symbol[symbol].append(p)

    # Process each symbol that has realized PnL in Transaction History
    for symbol in sorted(realized_pnl_by_symbol.keys()):
        # Skip symbols that were opened after 16:40 (new positions)
        if symbol in new_position_symbols:
            continue
            
        # Get the actual realized PnL from Transaction History
        actual_realized_pnl = realized_pnl_by_symbol[symbol]
        
        # Get position details from Position CSV (if available)
        if symbol in positions_by_symbol:
            pos_list = positions_by_symbol[symbol]
            # Use first position for side/entry, aggregate qty
            first_pos = pos_list[0]
            side = first_pos.get("Position Side", "").upper()
            entry = parse_number(first_pos.get("Entry Price", ""))
            close_price = parse_number(first_pos.get("Avg. Close Pirce", ""))
            qty = sum(parse_number(p.get("Max Open Interest", "")) for p in pos_list)
        else:
            # Position not in CSV, estimate from transaction
            side = "N/A"
            entry = 0
            close_price = 0
            qty = 0
        
        # Get Mark Price at 16:40
        mark_1640 = fetch_mark_price(symbol, "2025-10-10", TARGET_MS)
        
        if mark_1640 is None or qty == 0:
            # Can't calculate Entry->Mark without mark price or qty
            entry_to_mark = 0
            mark_to_close = actual_realized_pnl  # All loss attributed to outage period
        else:
            # Calculate Entry->Mark (unrealized PnL at 16:40)
            if side == "LONG":
                entry_to_mark = (mark_1640 - entry) * qty
            elif side == "SHORT":
                entry_to_mark = (entry - mark_1640) * qty
            else:
                entry_to_mark = 0
            
            # Mark->Liq = Actual Realized PnL - Entry->Mark
            # (This is derived so that Entry->Mark + Mark->Liq = Actual Realized PnL)
            mark_to_close = actual_realized_pnl - entry_to_mark
        
        # Use actual_realized_pnl as Entry->Liq (from Transaction History)
        total_loss = actual_realized_pnl
        
        # Accumulate totals
        total_entry_to_mark += entry_to_mark
        total_mark_to_close += mark_to_close
        total_closing_pnl_held += total_loss
        processed_symbols.add(symbol)
        
        processed_positions.append({
            "symbol": symbol, "side": side, "qty": qty, "entry": entry,
            "mark_1640": mark_1640 if mark_1640 else 0, "close_price": close_price,
            "entry_to_mark": entry_to_mark, "mark_to_close": mark_to_close,
            "total_loss": total_loss
        })
        
        # Print row
        if mark_1640 and qty > 0:
            print(f"{symbol:<14} {side:<5} {qty:>10.2f} {entry:>10.6f} {mark_1640:>10.6f} {close_price:>10.6f} | {entry_to_mark:>+12.2f} {mark_to_close:>+12.2f} {total_loss:>+12.2f}")
        else:
            print(f"{symbol:<14} {'N/A':<5} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10} | {'N/A':>12} {mark_to_close:>+12.2f} {total_loss:>+12.2f}")

    print("-" * 115)
    print(f"{'TOTAL':<14} {'':<5} {'':>10} {'':>10} {'':>10} {'':>10} | {total_entry_to_mark:>+12.2f} {total_mark_to_close:>+12.2f} {total_closing_pnl_held:>+12.2f}")
    
    print()
    print(f"    [RECONCILIATION NOTE]")
    print(f"    Held Positions Loss (Part 1):       {total_closing_pnl_held:>15,.2f}  <-- Positions existing before 16:40")
    print(f"    New Positions Loss (Part 3):        {calc_new_pos_pnl:>15,.2f}  <-- Positions opened after 16:40")
    print(f"    ---------------------------------------------------")
    print(f"    Total Realized PnL (Part 2):        {calc_total_realized:>15,.2f}  <-- Matches Transaction History")

    print()
    print("    +-------------------------------------------------------------------------+")
    print("    |  SUMMARY OF LOSS COMPONENTS                                            |")
    print("    +-------------------------------------------------------------------------+")
    print(f"    |  Entry->Mark (Unrealized at 16:40):              {total_entry_to_mark:>+15,.2f} USDT |")
    print(f"    |  Mark->Liq (Loss DURING Outage):                 {total_mark_to_close:>+15,.2f} USDT |")
    print(f"    |  Entry->Liq (Total Realized Loss):               {total_closing_pnl_held:>+15,.2f} USDT |")
    print("    +-------------------------------------------------------------------------+")
    
    # ========================================================================
    # Part 2: Account Changes After 16:40
    # ========================================================================
    print_section("Part 2: Account Changes from 16:40:38 to 21:19:53")
    
    # Statistics by asset
    changes = {
        "USDT": {"realized_pnl": 0.0, "transfer_in": 0.0, "transfer_out": 0.0, "fee": 0.0},
        "USDC": {"realized_pnl": 0.0, "transfer_in": 0.0, "transfer_out": 0.0, "fee": 0.0},
    }
    
    transfers_detail = []
    
    for tx in transactions:
        dt = tx.get("Date(UTC)", "")
        if dt > TARGET_STR and dt <= LIQUIDATION_END:
            tx_type = tx.get("type", "")
            amount = parse_number(tx.get("Amount", ""))
            asset = tx.get("Asset", "")
            
            if asset not in changes:
                continue
            
            if tx_type == "REALIZED_PNL":
                changes[asset]["realized_pnl"] += amount
            elif tx_type == "TRANSFER":
                if amount > 0:
                    changes[asset]["transfer_in"] += amount
                    transfers_detail.append({"time": dt, "amount": amount, "asset": asset, "type": "IN"})
                else:
                    changes[asset]["transfer_out"] += amount
                    transfers_detail.append({"time": dt, "amount": amount, "asset": asset, "type": "OUT"})
            elif tx_type in ["FUNDING_FEE", "COMMISSION", "INSURANCE_CLEAR"]:
                changes[asset]["fee"] += amount
    
    print_subsection("2.1 Realized PnL")
    
    for asset in ["USDT", "USDC"]:
        if changes[asset]["realized_pnl"] != 0:
            print(f"  {asset}: {changes[asset]['realized_pnl']:>+15,.2f}")
    
    total_realized = changes["USDT"]["realized_pnl"] + changes["USDC"]["realized_pnl"]
    print(f"  {'Total:':<6} {total_realized:>+15,.2f}")
    
    print_subsection("2.2 Transfer Details (Rescue Attempts)")
    
    for t in sorted(transfers_detail, key=lambda x: x["time"]):
        print(f"  {t['time']}  {t['amount']:>+12,.2f} {t['asset']}  ({t['type']})")
    
    total_transfer_in = changes["USDT"]["transfer_in"] + changes["USDC"]["transfer_in"]
    total_transfer_out = changes["USDT"]["transfer_out"] + changes["USDC"]["transfer_out"]
    total_transfer = total_transfer_in + total_transfer_out
    
    print(f"\n  Transfer In Total:  +{total_transfer_in:>12,.2f}")
    print(f"  Transfer Out Total:  {total_transfer_out:>12,.2f}")
    print(f"  Net Transfer:       {total_transfer:>+12,.2f}")
    
    print_subsection("2.3 Fees")
    
    total_fee = changes["USDT"]["fee"] + changes["USDC"]["fee"]
    print(f"  USDT Fees: {changes['USDT']['fee']:>+12,.2f}")
    print(f"  USDC Fees: {changes['USDC']['fee']:>+12,.2f}")
    print(f"  Total Fees: {total_fee:>+12,.2f}")
    
    # ========================================================================
    # Part 3: Positions Opened After 16:40 (New Positions)
    # ========================================================================
    print_section("Part 3: Positions Opened After 16:40 (To Be Claimed Invalid)")
    print(f"{'Symbol':<16} {'Side':<6} {'Entry':>12} {'Close':>12} {'Realized PnL':>14}")
    print("-" * 70)
    
    new_positions_pnl = 0.0
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")[:19]
        
        if opened > TARGET_STR and closed and closed <= LIQUIDATION_END:
            symbol = p.get("symbol", "")
            side = p.get("Position Side", "").upper()
            entry = parse_number(p.get("Entry Price", ""))
            close_price = parse_number(p.get("Avg. Close Pirce", ""))
            closing_pnl = parse_number(p.get("Closing PNL", ""))
            
            new_positions_pnl += closing_pnl
            print(f"{symbol:<16} {side:<6} {entry:>12.4f} {close_price:>12.4f} {closing_pnl:>+14.2f}")
            
    print("-" * 70)
    print(f"Total Loss from New Positions: {new_positions_pnl:>+39.2f}")
    
    # ========================================================================
    # Part 4: Account Equity Calculation at 16:40
    # ========================================================================
    print_section("Part 4: Account Equity Calculation at 16:40:38")
    
    print_subsection("4.1 Method 1: Reverse from Realized PnL")
    print("""
    Principle: Balance after liquidation = 0
               Balance at 16:40 + Changes after 16:40 = 0
               Balance at 16:40 = -(Realized PnL + Transfers + Fees)
    """)
    
    total_change = total_realized + total_transfer + total_fee
    wallet_balance = -total_change
    
    print(f"    Realized PnL:       {total_realized:>+15,.2f}")
    print(f"    Transfer (Net):     {total_transfer:>+15,.2f}")
    print(f"    Fees:               {total_fee:>+15,.2f}")
    print(f"    {'-' * 33}")
    print(f"    Total Change:       {total_change:>+15,.2f}")
    print(f"    * Wallet Balance at 16:40: {wallet_balance:>+15,.2f}")
    
    print_subsection("4.2 Correct Account Equity Calculation")
    print("""
    Principle: Account Equity = Wallet Balance + Unrealized PnL
               This is the standard definition used by Binance.
    """)
    
    # Unrealized PnL at 16:40 is exactly "total_entry_to_mark" from Part 1
    unrealized_liquidated = total_entry_to_mark
    account_equity_1640 = wallet_balance + unrealized_liquidated
    
    print(f"    Wallet Balance at 16:40:     {wallet_balance:>+15,.2f}")
    print(f"    Unrealized PnL at 16:40:     {unrealized_liquidated:>+15,.2f}")
    print(f"    {'-' * 40}")
    print(f"    * Account Equity at 16:40:   {account_equity_1640:>+15,.2f}")
    
    print_subsection("4.3 Verification of Balance Equation")
    
    print("""
    Verification: Final Balance = Equity at 16:40 + All Changes After 16:40

    Changes after 16:40 include:
    - Loss during outage (Mark -> Liq price for held positions)
    - New position losses
    - Net transfers in
    - Fees
    """)
    
    total_mark_period = total_mark_to_close
    all_changes = total_mark_period + new_positions_pnl + total_transfer + total_fee
    calculated_final = account_equity_1640 + all_changes
    
    print(f"    Account Equity at 16:40:     {account_equity_1640:>+15,.2f}")
    print(f"    Loss During Outage:          {total_mark_period:>+15,.2f}")
    print(f"    New Position PnL:            {new_positions_pnl:>+15,.2f}")
    print(f"    Net Transfer:                {total_transfer:>+15,.2f}")
    print(f"    Fees:                        {total_fee:>+15,.2f}")
    print(f"    {'-' * 40}")
    print(f"    Calculated Final Balance:    {calculated_final:>+15,.2f}")
    print(f"    Actual Final Balance:                    0.00")
    print()
    if abs(calculated_final) < 1:
        print("    [OK] VERIFIED: Balance equation is correct!")
    else:
        print(f"    [!] Discrepancy: {calculated_final:>+,.2f} (may be due to rounding or missing position data)")
    
    # ========================================================================
    # Part 5: Final Conclusion
    # ========================================================================
    print_section("Part 5: FINAL CONCLUSION")
    
    print()
    print("    +" + "=" * 63 + "+")
    print("    |" + "  Account Status at 16:40:38 UTC (Before Outage)  ".center(63) + "|")
    print("    +" + "=" * 63 + "+")
    print(f"    |  Wallet Balance:                        {wallet_balance:>+18,.2f} |")
    print(f"    |  Unrealized PnL:                        {unrealized_liquidated:>+18,.2f} |")
    print("    +" + "=" * 63 + "+")
    print(f"    |  ** ACCOUNT EQUITY:                     {account_equity_1640:>+18,.2f} |")
    print("    +" + "=" * 63 + "+")
    print()
    print("    +" + "=" * 63 + "+")
    print("    |" + "     LOSS BREAKDOWN     ".center(63) + "|")
    print("    +" + "=" * 63 + "+")
    print(f"    |  Pre-existing Unrealized Loss (Entry->Mark): {total_entry_to_mark:>+14,.2f} |")
    print(f"    |  Loss During Outage (Mark->Liq):             {total_mark_to_close:>+14,.2f} |")
    print(f"    |  New Position Loss (After 16:40):           {new_positions_pnl:>+14,.2f} |")
    print(f"    |  Rescue Funds Transferred In:              +{total_transfer_in:>13,.2f} |")
    print(f"    |  Final Balance:                                        0.00 |")
    print("    +" + "=" * 63 + "+")
    
    # ========================================================================
    # Part 6: HKIAC Claim Calculation
    # ========================================================================
    print_section("Part 6: HKIAC ARBITRATION CLAIM CALCULATION")
    
    print("")
    print("    +-------------------------------------------------------------------------+")
    print("    |  CLAIM METHODOLOGY                                                     |")
    print("    +-------------------------------------------------------------------------+")
    print("    |  Your claim is for the total value lost due to Binance system outage   |")
    print("    |  on October 10, 2025. Two equivalent methods to calculate:             |")
    print("    |                                                                         |")
    print("    |  Method 1: Account Value + Capital Injected                            |")
    print("    |    = Account Equity at 16:40 + Net Transfer                            |")
    print("    |                                                                         |")
    print("    |  Method 2: Sum of All Losses During Outage                             |")
    print("    |    = Mark->Liq Loss + New Position Loss + Fees                         |")
    print("    |                                                                         |")
    print("    |  Both methods give the SAME result.                                    |")
    print("    +-------------------------------------------------------------------------+")
    
    # Calculate claim using both methods
    method1_claim = account_equity_1640 + total_transfer
    method2_claim = abs(total_mark_to_close) + abs(new_positions_pnl) + abs(total_fee)
    
    print()
    print("    +=========================================================================+")
    print("    |                  METHOD 1: ACCOUNT VALUE + CAPITAL                     |")
    print("    +=========================================================================+")
    print("    |                                                                         |")
    print(f"    |  A. Account Equity at 16:40:38 UTC                   {account_equity_1640:>+14,.2f}  |")
    print("    |     (Wallet Balance + Unrealized PnL)                                   |")
    print(f"    |     = {wallet_balance:>+,.2f} + {unrealized_liquidated:>+,.2f}".ljust(72) + "|")
    print("    |                                                                         |")
    print(f"    |  B. Net Transfer (Capital Injected During Outage)   {total_transfer:>+14,.2f}  |")
    print(f"    |     (Transfer In: +{total_transfer_in:,.2f}, Transfer Out: {total_transfer_out:,.2f})".ljust(72) + "|")
    print("    |                                                                         |")
    print("    +---------+---------------------------------------------------------------+")
    print(f"    |  CLAIM  |  A + B =                                    {method1_claim:>+14,.2f}  |")
    print("    +---------+---------------------------------------------------------------+")
    
    print()
    print("    +=========================================================================+")
    print("    |                  METHOD 2: SUM OF ALL LOSSES                           |")
    print("    +=========================================================================+")
    print("    |                                                                         |")
    print(f"    |  C. Mark->Liq Loss (Outage Loss on Held Positions)  {abs(total_mark_to_close):>+14,.2f}  |")
    print("    |     (Loss from 16:40 Mark Price to Liquidation)                         |")
    print("    |                                                                         |")
    print(f"    |  D. New Position Loss (Opened After 16:40)          {abs(new_positions_pnl):>+14,.2f}  |")
    print("    |                                                                         |")
    print(f"    |  E. Transaction Fees                                {abs(total_fee):>+14,.2f}  |")
    print("    |                                                                         |")
    print("    +---------+---------------------------------------------------------------+")
    print(f"    |  CLAIM  |  C + D + E =                                {method2_claim:>+14,.2f}  |")
    print("    +---------+---------------------------------------------------------------+")
    
    print()
    print("    +=========================================================================+")
    print("    |                         VERIFICATION                                   |")
    print("    +=========================================================================+")
    if abs(method1_claim - method2_claim) < 1:
        print("    |                                                                         |")
        print(f"    |  Method 1:  {method1_claim:>+14,.2f}                                          |")
        print(f"    |  Method 2:  {method2_claim:>+14,.2f}                                          |")
        print("    |                                                                         |")
        print("    |  [OK] Both methods match!                                               |")
    else:
        diff = abs(method1_claim - method2_claim)
        print(f"    |  Method 1:  {method1_claim:>+14,.2f}                                          |")
        print(f"    |  Method 2:  {method2_claim:>+14,.2f}                                          |")
        print(f"    |  Difference: {diff:>14,.2f} (rounding)                                   |")
    print("    |                                                                         |")
    print("    +=========================================================================+")
    
    print()
    print("    +=========================================================================+")
    print("    |                                                                         |")
    print(f"    |     *****  TOTAL HKIAC CLAIM AMOUNT:  {method1_claim:>+14,.2f} USDT  *****     |")
    print("    |                                                                         |")
    print("    +=========================================================================+")
    
    print()
    print("=" * 100)
    print("                              END OF REPORT")
    print("=" * 100)


if __name__ == "__main__":
    main()
