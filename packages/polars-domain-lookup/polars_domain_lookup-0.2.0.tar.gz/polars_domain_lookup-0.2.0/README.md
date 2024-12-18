# Polars Domain Lookup Plugin

This plugin extends the functionality of [Polars](https://www.pola.rs) by providing a method to check whether domains are included in a predefined list of the top 1,000,000 domains. The result is returned as a boolean value (True/False).

## Features

- **Domain Lookup:** Checks if the provided domains are included in a list of the top 1,000,000 domains.
- **Integration with Polars:** Works seamlessly with Polars DataFrames, offering fast processing.

## Requirements

- Python 3.8+
- Polars library

Install Polars with:

```bash
uv add polars
```

- Top 1 Million Domains List: The domain list must be provided as a file (e.g., `cloudflare-radar_top-1000000-domains.csv`) in CSV format. This file can be downloaded from sources like [Cloudflare Radar](https://radar.cloudflare.com/domains).

## Installation

Add the plugin to your project. Install it directly from the repository or manually include the Python file.

```bash
uv add polars-domain-lookup
```

## Usage

### Example Code

```python
import polars as pl
from polars_domain_lookup import is_common_domain

# Example DataFrame with domains
df = pl.DataFrame({
    "domains": ["example.com", "google.com", "nonexistentdomain.xyz"]
})

# Load the top 1,000,000 domains list
top_domains_path = "cloudflare-radar_top-1000000-domains.csv"

# Perform the lookup
df = df.with_columns(
    is_common_domain(df["domains"]).alias("is_top_domain")
)

print(df)
```

### Output

If `cloudflare-radar_top-1000000-domains.csv` contains `google.com`, the output will look like this:

```
shape: (3, 2)
┌───────────────────────┬───────────────┐
│ domains               │ is_top_domain │
├───────────────────────┼───────────────┤
│ example.com           │ false         │
│ google.com            │ true          │
│ nonexistentdomain.xyz │ false         │
└───────────────────────┴───────────────┘
```

