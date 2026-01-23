# pip install tardis-dev
# requires Python >=3.6
from tardis_dev import datasets, get_exchange_details
import logging

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)


# function used by default if not provided via options
def default_file_name(exchange, data_type, date, symbol, format):
    return f"{exchange}_{data_type}_{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"


# customized get filename function - saves data in nested directory structure
def file_name_nested(exchange, data_type, date, symbol, format):
    return f"{exchange}/{data_type}/{date.strftime('%Y-%m-%d')}_{symbol}.{format}.gz"


# returns data available at https://api.tardis.dev/v1/exchanges/okex-futures
okex_futures_details = get_exchange_details("okex-futures")
# print(okex_futures_details)

# Download futures/depth channel
datasets.download(
    exchange="okex-futures",
    data_types=[
        "futures/depth",
    ],
    from_date="2025-10-10",
    to_date="2025-10-11",
    symbols=["BTC-USDT"],
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    download_dir="./datasets",
)

print("Downloaded futures/depth")

# Download futures/depth_l2_tbt channel
datasets.download(
    exchange="okex-futures",
    data_types=[
        "futures/depth_l2_tbt",
    ],
    from_date="2025-10-10",
    to_date="2025-10-11",
    symbols=["BTC-USDT"],
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    download_dir="./datasets",
)

print("Downloaded futures/depth_l2_tbt")
print("All downloads finished")
