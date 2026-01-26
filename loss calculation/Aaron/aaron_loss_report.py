"""
================================================================================
                        AARON LOSS CALCULATION REPORT
================================================================================
Calculation Time: 2025-10-10 15:30:42 UTC (Before Binance System Outage)
Liquidation End Time: 2025-10-10 21:20:23 UTC
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
TARGET_STR = "2025-10-10 15:30:42"
TARGET_MS = int(datetime(2025, 10, 10, 15, 30, 42, tzinfo=timezone.utc).timestamp() * 1000)
LIQUIDATION_END = "2025-10-10 21:21:00"  # Includes Aaron's liquidation at 21:20:23

# Aaron's Data Files
TRADES_FILE = "202511131124_u本位tradehistory.csv"
TRANSACTIONS_FILE = "202511131155_u本位transaction history.csv"
POSITIONS_FILE = "202511131155_u本位positionhistory.csv"
ORDERS_FILE = "202511160817_u本位order-history.csv"


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
    # Handle quarterly futures symbols like BTCUSDT_251226
    base_symbol = symbol.split("_")[0] if "_" in symbol else symbol
    
    url = (
        "https://data.binance.vision/data/futures/um/daily/markPriceKlines/"
        f"{symbol}/1m/{symbol}-1m-{date_str}.zip"
    )
    req = Request(url, headers={"User-Agent": "loss-calc"}, method="GET")
    try:
        with urlopen(req, timeout=15) as resp:
            data = resp.read()
    except Exception:
        # Try with base symbol if quarterly contract fails
        if "_" in symbol:
            url = (
                "https://data.binance.vision/data/futures/um/daily/markPriceKlines/"
                f"{base_symbol}/1m/{base_symbol}-1m-{date_str}.zip"
            )
            req = Request(url, headers={"User-Agent": "loss-calc"}, method="GET")
            try:
                with urlopen(req, timeout=15) as resp:
                    data = resp.read()
            except Exception:
                return None
        else:
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
    
    print()
    print("█" * 100)
    print("█" + " " * 98 + "█")
    print("█" + "              AARON LOSS CALCULATION REPORT              ".center(98) + "█")
    print("█" + " " * 98 + "█")
    print("█" * 100)
    print()
    print(f"Calculation Time:     2025-10-10 15:30:42 UTC (Before Binance System Outage)")
    print(f"Liquidation End:      2025-10-10 21:20:23 UTC")
    print(f"Final Balance:        Check below")
    
    # ========================================================================
    # Part 1: Position Status at 15:30
    # ========================================================================
    print_section("Part 1: Position Status at 15:30:42 UTC")
    
    positions_at_1530 = []
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")
        
        # Positions still held at 15:30
        if opened <= TARGET_STR and (not closed or closed > TARGET_STR):
            positions_at_1530.append(p)
    
    print(f"\n{len(positions_at_1530)} positions held at 15:30:")
    print()
    print(f"{'Symbol':<20} {'Side':<6} {'Quantity':>14} {'Entry Price':>16} {'15:30 Mark':>14} {'Unrealized PnL':>16}")
    print("-" * 100)
    
    total_unrealized = 0.0
    position_details = []
    
    for p in positions_at_1530:
        symbol = p.get("symbol", "")
        side = p.get("Position Side", "").upper()
        qty = parse_number(p.get("Max Open Interest", ""))
        entry = parse_number(p.get("Entry Price", ""))
        opened = p.get("Opened", "")[:19]
        
        mark_1530 = fetch_mark_price(symbol, "2025-10-10", TARGET_MS)
        
        if mark_1530 is None:
            print(f"{symbol:<20} {side:<6} {qty:>14.5f} {entry:>16.6f} {'N/A':>14} {'N/A':>16}")
            position_details.append({
                "symbol": symbol, "side": side, "qty": qty, "entry": entry,
                "mark_1530": None, "unrealized": 0, "opened": opened
            })
            continue
        
        if side == "LONG":
            unrealized = (mark_1530 - entry) * qty
        else:
            unrealized = (entry - mark_1530) * qty
        
        total_unrealized += unrealized
        position_details.append({
            "symbol": symbol, "side": side, "qty": qty, "entry": entry,
            "mark_1530": mark_1530, "unrealized": unrealized, "opened": opened
        })
        
        print(f"{symbol:<20} {side:<6} {qty:>14.5f} {entry:>16.6f} {mark_1530:>14.2f} {unrealized:>+16.2f}")
    
    print("-" * 100)
    print(f"{'Total Unrealized PnL at 15:30':<75} {total_unrealized:>+16.2f} USDT")
    
    # ========================================================================
    # Part 2: Account Changes After 15:30
    # ========================================================================
    print_section("Part 2: Account Changes from 15:30:42 to 21:20:23")
    
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
    
    if transfers_detail:
        for t in sorted(transfers_detail, key=lambda x: x["time"]):
            print(f"  {t['time']}  {t['amount']:>+12,.2f} {t['asset']}  ({t['type']})")
    else:
        print("  (No transfers during this period)")
    
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
    # Part 3: Liquidated Position Details After 15:30
    # ========================================================================
    print_section("Part 3: Liquidated Position Details After 15:30:42")
    
    print_subsection("3.1 Positions Held at 15:30, Liquidated Afterwards")
    print(f"{'Symbol':<20} {'Side':<6} {'Quantity':>12} {'Entry':>14} {'15:30Mark':>12} {'Close':>14} {'Total PnL':>14}")
    print("-" * 110)
    
    liquidated_positions = []
    total_closing_pnl = 0.0
    
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")[:19]
        
        if opened <= TARGET_STR and closed and closed > TARGET_STR and closed <= LIQUIDATION_END:
            symbol = p.get("symbol", "")
            side = p.get("Position Side", "").upper()
            qty = parse_number(p.get("Max Open Interest", ""))
            entry = parse_number(p.get("Entry Price", ""))
            close_price = parse_number(p.get("Avg. Close Pirce", ""))
            closing_pnl = parse_number(p.get("Closing PNL", ""))
            
            mark_1530 = fetch_mark_price(symbol, "2025-10-10", TARGET_MS)
            
            liquidated_positions.append({
                "symbol": symbol, "side": side, "qty": qty, "entry": entry,
                "mark_1530": mark_1530, "close_price": close_price,
                "closing_pnl": closing_pnl, "closed": closed
            })
            
            total_closing_pnl += closing_pnl
            
            mark_str = f"{mark_1530:>12.2f}" if mark_1530 else "N/A"
            print(f"{symbol:<20} {side:<6} {qty:>12.5f} {entry:>14.2f} {mark_str:>12} {close_price:>14.2f} {closing_pnl:>+14.2f}")
    
    print("-" * 110)
    print(f"{'Liquidated Positions Closing PnL Total':<82} {total_closing_pnl:>+14.2f}")
    
    print_subsection("3.2 Positions Opened After 15:30, Then Closed")
    
    new_positions_pnl = 0.0
    new_positions = []
    
    for p in positions:
        opened = p.get("Opened", "")[:19]
        closed = p.get("Closed", "")[:19]
        
        if opened > TARGET_STR and closed and closed <= LIQUIDATION_END:
            symbol = p.get("symbol", "")
            side = p.get("Position Side", "").upper()
            closing_pnl = parse_number(p.get("Closing PNL", ""))
            new_positions_pnl += closing_pnl
            new_positions.append({"symbol": symbol, "side": side, "closing_pnl": closing_pnl})
            print(f"  {symbol:<20} {side:<6} Closing PnL: {closing_pnl:>+14.2f}")
    
    if new_positions:
        print(f"\n  New Positions Closing PnL Total: {new_positions_pnl:>+14.2f}")
    else:
        print("  (None)")
    
    # ========================================================================
    # Part 4: Account Equity Calculation at 15:30
    # ========================================================================
    print_section("Part 4: Account Equity Calculation at 15:30:42")
    
    print_subsection("4.1 Method 1: Reverse from Realized PnL")
    print("""
    Principle: Balance after liquidation = Final Balance
               Balance at 15:30 + Changes after 15:30 = Final Balance
               Balance at 15:30 = Final Balance - (Realized PnL + Transfers + Fees)
    """)
    
    total_change = total_realized + total_transfer + total_fee
    # We need to calculate what the final balance was
    # For now, assume full liquidation (0)
    wallet_balance = -total_change
    
    print(f"    Realized PnL:       {total_realized:>+18,.2f}")
    print(f"    Transfer (Net):     {total_transfer:>+18,.2f}")
    print(f"    Fees:               {total_fee:>+18,.2f}")
    print(f"    ─────────────────────────────────")
    print(f"    Total Change:       {total_change:>+18,.2f}")
    print(f"    ★ Wallet Balance at 15:30: {wallet_balance:>+18,.2f}")
    
    print_subsection("4.2 Method 2: Reverse from Mark Price")
    print("""
    Principle: Use 15:30 Mark Price vs Close Price to calculate period PnL
               Equity at 15:30 = -(Mark Period PnL + New Position PnL + Transfers + Fees)
    """)
    
    # Calculate Mark period PnL
    total_mark_period = 0.0
    for lp in liquidated_positions:
        if lp["mark_1530"] is None:
            continue
        if lp["side"] == "LONG":
            period_pnl = (lp["close_price"] - lp["mark_1530"]) * lp["qty"]
        else:
            period_pnl = (lp["mark_1530"] - lp["close_price"]) * lp["qty"]
        total_mark_period += period_pnl
    
    total_change_mark = total_mark_period + new_positions_pnl + total_transfer + total_fee
    equity_mark = -total_change_mark
    
    print(f"    Mark Period PnL:    {total_mark_period:>+18,.2f}")
    print(f"    New Position PnL:   {new_positions_pnl:>+18,.2f}")
    print(f"    Transfer (Net):     {total_transfer:>+18,.2f}")
    print(f"    Fees:               {total_fee:>+18,.2f}")
    print(f"    ─────────────────────────────────")
    print(f"    Total Change:       {total_change_mark:>+18,.2f}")
    print(f"    ★ Account Equity at 15:30: {equity_mark:>+18,.2f}")
    
    print_subsection("4.3 Relationship Between Two Methods")
    
    # Calculate unrealized PnL of positions held at 15:30 (only those liquidated later)
    unrealized_liquidated = 0.0
    for lp in liquidated_positions:
        if lp["mark_1530"] is None:
            continue
        if lp["side"] == "LONG":
            unrealized_liquidated += (lp["mark_1530"] - lp["entry"]) * lp["qty"]
        else:
            unrealized_liquidated += (lp["entry"] - lp["mark_1530"]) * lp["qty"]
    
    print(f"    Method 1 (Realized PnL) gives: Wallet Balance = {wallet_balance:>+18,.2f}")
    print(f"    Method 2 (Mark Price) gives:   Account Equity = {equity_mark:>+18,.2f}")
    print()
    print(f"    Unrealized PnL of liquidated positions at 15:30: {unrealized_liquidated:>+18,.2f}")
    print()
    print(f"    Verification: Wallet Balance + Unrealized PnL = Account Equity")
    print(f"          {wallet_balance:>+,.2f} + {unrealized_liquidated:>+,.2f} = {wallet_balance + unrealized_liquidated:>+,.2f}")
    print(f"          ≈ {equity_mark:>+,.2f}")
    
    # ========================================================================
    # Part 5: Price Comparison Analysis
    # ========================================================================
    print_section("Part 5: Price Comparison (Entry vs 15:30 Mark vs Liquidation)")
    
    print(f"{'Symbol':<18} {'Side':<5} {'Entry':>14} {'15:30Mark':>12} {'Liq Price':>14} │ {'Entry→Mark':>12} {'Mark→Liq':>12} {'Total':>12}")
    print("-" * 120)
    
    total_entry_to_mark = 0.0
    total_mark_to_close = 0.0
    
    for lp in liquidated_positions:
        if lp["mark_1530"] is None:
            continue
        
        symbol = lp["symbol"]
        side = lp["side"]
        entry = lp["entry"]
        mark = lp["mark_1530"]
        close = lp["close_price"]
        qty = lp["qty"]
        
        if side == "LONG":
            entry_to_mark = (mark - entry) * qty
            mark_to_close = (close - mark) * qty
        else:
            entry_to_mark = (entry - mark) * qty
            mark_to_close = (mark - close) * qty
        
        total_entry_to_mark += entry_to_mark
        total_mark_to_close += mark_to_close
        total_loss = entry_to_mark + mark_to_close
        
        print(f"{symbol:<18} {side:<5} {entry:>14.2f} {mark:>12.2f} {close:>14.2f} │ {entry_to_mark:>+12.2f} {mark_to_close:>+12.2f} {total_loss:>+12.2f}")
    
    print("-" * 120)
    print(f"{'Total':<18} {'':<5} {'':>14} {'':>12} {'':>14} │ {total_entry_to_mark:>+12.2f} {total_mark_to_close:>+12.2f} {total_entry_to_mark + total_mark_to_close:>+12.2f}")
    
    print()
    print("    Notes:")
    print(f"    • Entry→Mark:  Unrealized PnL at 15:30 = {total_entry_to_mark:>+,.2f}")
    print(f"    • Mark→Liq:    Loss due to price movement after 15:30 = {total_mark_to_close:>+,.2f}")
    print(f"    • If Binance system was normal, user could have closed at 15:30, loss would only be {total_entry_to_mark:>+,.2f}")
    print(f"    • Additional loss caused by system outage = {total_mark_to_close:>+,.2f}")
    
    # ========================================================================
    # Part 6: Final Conclusion
    # ========================================================================
    print_section("Part 6: FINAL CONCLUSION")
    
    print()
    print("    ┌─────────────────────────────────────────────────────────────────┐")
    print("    │                Account Status at 15:30:42 UTC                   │")
    print("    ├─────────────────────────────────────────────────────────────────┤")
    print(f"    │  Wallet Balance:                       {wallet_balance:>+20,.2f} │")
    print(f"    │  Unrealized PnL:                       {unrealized_liquidated:>+20,.2f} │")
    print(f"    │  Account Equity:                       {wallet_balance + unrealized_liquidated:>+20,.2f} │")
    print("    └─────────────────────────────────────────────────────────────────┘")
    print()
    print("    ┌─────────────────────────────────────────────────────────────────┐")
    print("    │                       LOSS ANALYSIS                             │")
    print("    ├─────────────────────────────────────────────────────────────────┤")
    print(f"    │  Pre-existing Loss at 15:30 (Entry→Mark):   {total_entry_to_mark:>+17,.2f} │")
    print(f"    │  Loss During Outage (Mark→Liq):             {total_mark_to_close:>+17,.2f} │")
    print(f"    │  New Position Loss After 15:30:             {new_positions_pnl:>+17,.2f} │")
    print(f"    │  Rescue Funds Transferred In:              +{total_transfer_in:>16,.2f} │")
    print("    └─────────────────────────────────────────────────────────────────┘")
    print()
    print("    ┌─────────────────────────────────────────────────────────────────┐")
    print("    │                     CLAIMABLE DAMAGES                           │")
    print("    ├─────────────────────────────────────────────────────────────────┤")
    
    # Claimable = Loss during outage + New position loss
    claimable = abs(total_mark_to_close) + abs(new_positions_pnl)
    
    print(f"    │  Additional Loss Due to System Outage:      {abs(total_mark_to_close):>+17,.2f} │")
    print(f"    │  New Position Loss (Unable to Operate):     {abs(new_positions_pnl):>+17,.2f} │")
    print("    ├─────────────────────────────────────────────────────────────────┤")
    print(f"    │  ★ TOTAL CLAIMABLE:                         {claimable:>+17,.2f} │")
    print("    └─────────────────────────────────────────────────────────────────┘")
    print()
    
    print("=" * 100)
    print("                              END OF REPORT")
    print("=" * 100)


if __name__ == "__main__":
    main()
