from dagster import Definitions, load_assets_from_package_module

from .country_lifestyle_analytics import assets

# Load all assets
dagster_assets = load_assets_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=dagster_assets
)