# Liquidity Orderbook Viewer

Lightweight viewer and analysis scripts for comparing BTC order books across venues on 2025-10-10.

## Setup

```bash
pip install -r requirements.txt
```

## How to run the viewer

From this folder:

```bash
python .\orderbook_viewer.py
```

This launches the local web UI. The templates live in `templates/`, and static assets are under `static/`.

## Data

Datasets are large and omitted from the repo. Download them here:
[Drive link](https://drive.google.com/file/d/1muAQfUgQaJyCqPR55pU9U_yqHY7uXY9b/view?usp=sharing)

After download, place the extracted `datasets/Oct 10/` under this folder so the scripts can read them. Update the paths in `orderbook_viewer.py` if you add new venues or dates.

## Utilities

- `analyze_*` scripts: quick analyses for spreads, liquidity drops, and depth ranges.
- `downloads/`: helpers to fetch raw order book snapshots from multiple exchanges.
