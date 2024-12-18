from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from polars_domain_lookup._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_domain_lookup.typing import IntoExprColumn

LIB = Path(__file__).parent


def is_common_domain(expr: IntoExprColumn, top_domains_file: str) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="is_common_domain",
        is_elementwise=True,
        kwargs={"top_domains_file": top_domains_file},
    )

