# pip install tardis-dev
# requires Python >=3.6
from tardis_dev import datasets, get_exchange_details
import logging

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)


# function used by default if not provided via options
def default_file_name(exchange, data_type, date, symbol, format):
    return f"{exchange}_{data_type}_{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"


# returns data available at https://api.tardis.dev/v1/exchanges/okex-swap
okex_swap_details = get_exchange_details("okex-swap")
# print(okex_swap_details)

datasets.download(
    exchange="okex-swap",
    data_types=[
        "book_snapshot_25",
        "derivative_ticker",
        "book_ticker",
        "incremental_book_L2",
    ],
    from_date="2025-10-10",
    to_date="2025-10-11",
    symbols=["BTC-USDC-SWAP"],
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    download_dir="./datasets",
)

print("Download finished for BTC-USDC-SWAP")
