df["ts"] = pd.to_datetime(df["timestamp"], unit="us", utc=True)
# Options data notes

- Timestamps in the options_chain CSV files are Unix epoch in microseconds (UTC). You can search a value directly, e.g. `1760131254345000`.
- Convert to human time with pandas:

```python
import pandas as pd
pd.to_datetime(1760131254345000, unit="us", utc=True)
# 2025-10-10 21:20:54.345000+00:00 (Friday, October 10, 2025 9:20:54.345 PM UTC)
```
- Filtering around a time window:

```python
import pandas as pd
from pathlib import Path
path = Path("datasets_options/okex-options_options_chain_2025-10-10_BTC-USD-251128-132000-C.csv.gz")
df = pd.read_csv(path)
df["ts"] = pd.to_datetime(df["timestamp"], unit="us", utc=True)
window = df[(df["ts"] >= "2025-10-10 21:20:00+00:00") & (df["ts"] <= "2025-10-10 21:21:00+00:00")]
print(window.head())
```

- List of OKX option symbols/exchanges from Tardis: https://api.tardis.dev/v1/exchanges/okex-options (returns metadata; helpful to check symbols before downloading).

- Observation (OKX sample around 2025-10-10 09:20 UTC): I did not see evidence of bids materially exceeding asks or trades clearing at prices absurdly higher than Black-Scholes fair value.