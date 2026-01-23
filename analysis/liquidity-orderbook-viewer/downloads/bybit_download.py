# pip install tardis-dev
# requires Python >=3.6
from tardis_dev import datasets, get_exchange_details
import logging

# comment out to disable debug logs
logging.basicConfig(level=logging.DEBUG)

datasets.download(
    exchange="bybit",
    data_types=[
        "book_snapshot_25",
    ],
    from_date="2025-10-10",
    to_date="2025-10-11",
    symbols=["BTCPERP"],
    api_key="TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ",
    download_dir="./datasets",
)

print("Download finished for Bybit BTCPERP")
