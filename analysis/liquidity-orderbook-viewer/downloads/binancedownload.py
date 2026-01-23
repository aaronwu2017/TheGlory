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


# returns data available at https://api.tardis.dev/v1/exchanges/binance-futures
binance_futures_details = get_exchange_details("binance-futures")
# print(binance_futures_details)

datasets.download(
    # one of https://api.tardis.dev/v1/exchanges with supportsDatasets:true
    exchange="binance-futures",
    # accepted data types - check binance_futures_details["datasets"]["symbols"][]["dataTypes"]
    data_types=[
        "book_snapshot_25",
    ],
    # change date ranges as needed to fetch full month or year for example
    from_date="2025-10-10",
    # to date is non inclusive
    to_date="2025-10-11",
    # accepted values: 'datasets.symbols[].id' field
    symbols=["BTCUSDC"],
    # your API key to get access to non sample data
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    # (optional) path where data will be downloaded into, default dir is './datasets'
    download_dir="./datasets",
    # (optional) - customize downloaded file name/path
    # get_filename=default_file_name,
    # (optional) file_name_nested will download data to nested directory structure
    # get_filename=file_name_nested,
)

print("Download finished for Binance BTCUSDC")
