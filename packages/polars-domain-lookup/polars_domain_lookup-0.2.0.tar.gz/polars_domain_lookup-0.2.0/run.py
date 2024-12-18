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
    is_common_domain(df["domains"], top_domains_file="cloudflare-radar_top-1000000-domains.csv").alias("is_common_domain")
)

print(df)