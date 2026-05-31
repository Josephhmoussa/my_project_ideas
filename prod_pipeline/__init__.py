from dagster import Definitions, load_assets_from_package_module
from dotenv import load_dotenv
import os

from . import assets
from .resources.dbt_resource import dbt_resource


# Load all assets
dagster_assets = load_assets_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=dagster_assets,
    resources={"dbt": dbt_resource}
)