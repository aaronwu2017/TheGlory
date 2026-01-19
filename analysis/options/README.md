# Options data notes

- Timestamps in the options_chain CSV files are Unix epoch in microseconds (UTC). You can search a value directly, e.g. `1760131254345000`.


- List of OKX option symbols/exchanges from Tardis: https://api.tardis.dev/v1/exchanges/okex-options (returns metadata; helpful to check symbols before downloading).

- Observation (OKX sample around 2025-10-10 09:20 UTC): I did not see evidence of bids materially exceeding asks or trades clearing at prices absurdly higher than Black-Scholes fair value.