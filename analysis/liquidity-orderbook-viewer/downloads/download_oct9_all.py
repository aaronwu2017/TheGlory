from tardis_dev import datasets
import logging

logging.basicConfig(level=logging.INFO)

API_KEY = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"

# Download all exchanges for October 9, 2025
datasets.download(
    exchange="binance-futures",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTCUSDT", "BTCUSDC"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="okex-swap",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTC-USDT-SWAP", "BTC-USDC-SWAP"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="bybit",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTCPERP"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="huobi-dm-linear-swap",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTC-USDT"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="kucoin-futures",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["XBTUSDCM"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="hyperliquid",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTC"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="bitget-futures",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTCUSDT"],
    api_key=API_KEY,
    download_dir="./datasets"
)

datasets.download(
    exchange="coinbase-international",
    data_types=["book_snapshot_25"],
    from_date="2025-10-09",
    to_date="2025-10-09",
    symbols=["BTC-PERP"],
    api_key=API_KEY,
    download_dir="./datasets"
)

print("All October 9 downloads complete!")
