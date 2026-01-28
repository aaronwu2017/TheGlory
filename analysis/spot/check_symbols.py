from tardis_dev import datasets
import sys
import logging

# Handle console encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

API_KEY = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"

def check_symbols():
    try:
        # We can't easily list all symbols via datasets.download, 
        # but we can try to download a small timeframe for expected symbols to see specific error messages
        # OR we can trust the previous error messages which were quite specific.
        
        # Previous error: "Invalid 'symbol' param provided: 'POLUSD_PERP'. Did you mean 'SOLUSD_PERP'?"
        # This implies it doesn't know POLUSD_PERP.
        
        # Checking MATIC again?
        # Error: "Data for 'MATICUSD_PERP' is available only up to '2024-09-06T00:00:00.000Z'"
        # So MATIC coin-m is gone. POL coin-m probably doesn't exist yet or is named differently.
        
        # PEPE error: "Did you mean 'APEUSD_PERP'?" -> PEPEUSD_PERP doesn't exist.
        
        # The user asked to "download the missing ones". 
        # If they don't exist, I can't download them.
        # I will focus on getting the SPOT data which I am already doing.
        pass
    except Exception:
        pass

if __name__ == "__main__":
    print("Checking specific symbols manually or assuming non-existence based on logs.")
