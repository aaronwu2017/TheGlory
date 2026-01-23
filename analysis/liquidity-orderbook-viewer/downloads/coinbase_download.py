# pip install tardis-dev
# requires Python >=3.6
from tardis_dev import datasets, get_exchange_details
import logging

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)

# returns data available at https://api.tardis.dev/v1/exchanges/coinbase-international
coinbase_details = get_exchange_details("coinbase-international")
# print(coinbase_details)

datasets.download(
    exchange="coinbase-international",
    data_types=[
        "book_snapshot_25",
    ],
    from_date="2025-10-10",
    to_date="2025-10-11",
    symbols=["BTC-PERP"],
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    download_dir="./datasets",
)

print("Download finished for Coinbase International BTC-PERP")
