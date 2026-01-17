from tardis_dev import datasets
import logging
import os

# Configure logging to see download progress
logging.basicConfig(level=logging.DEBUG)

def download_options_chain():
    """
    Downloads option chain data including Bid/Ask, Mark Price, and Greeks (Black-Scholes).
    """
    # The API Key you provided
    api_key = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"
    
    # Exchange: 'deribit' is the standard for crypto options.
    # Alternative: 'okex-options'
    target_exchange = "okex-options"

    # Ensure the download directory exists and use an absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(script_dir, "datasets_options")
    os.makedirs(download_dir, exist_ok=True)

    print(f"Starting download for {target_exchange} options chain...")
    print(f"Saving to: {download_dir}")
    print(f"Using API Key: {api_key[:5]}... (Check if this key has access to the requested dates)")

    datasets.download(
        exchange=target_exchange,
        
        # 'options_chain' is the specific data type that includes:
        # - bid_price, ask_price
        # - mark_price
        # - bid_iv, ask_iv, mark_iv (Implied Volatility)
        # - delta, gamma, vega, theta, rho (Black-Scholes Greeks)
        data_types=["options_chain"],
        
        # Date range from your example
        from_date="2025-10-10",
        to_date="2025-10-11",
        
        # Leaving 'symbols' empty downloads ALL active options for that day (The full Chain).
        # If you specify symbols, you must use exact contract names (e.g., ["BTC-29DEC23-30000-C"]).
        # RECOMMENDATION: Leave empty to download all, then filter for "BTC" in your analysis code.
        # (Listing all historical option symbols manually is very difficult).
        symbols=["BTC-USD-251128-132000-C"],
        api_key=api_key,
        download_dir=download_dir
    )
    print(f"Download finished! Check the '{download_dir}' folder.")
    
    # Verify if files were actually downloaded
    if os.path.exists(download_dir) and os.listdir(download_dir):
        print(f"Success: Found {len(os.listdir(download_dir))} files.")
    else:
        print("Warning: No files found. Ensure the date is in the past and the API key has access.")

if __name__ == "__main__":
    download_options_chain()