from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import DbtCliResource

from . import assets
from .resources.dbt_resource import timesheet_dbt_resource


# Load all assets
dagster_assets = load_assets_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=dagster_assets,
    resources={
        "timesheet_dbt": timesheet_dbt_resource
    }
)