import polars as pl
from polars_cisco_umrella import is_common_domain


df = pl.DataFrame(
    {
        "dns": ["github.com", "google.de", "blub.com", "heise.de"],
    }
)

result = df.with_columns(is_in_cisco_umbrella=is_common_domain("dns", "top-1m.csv"))
print(result)
