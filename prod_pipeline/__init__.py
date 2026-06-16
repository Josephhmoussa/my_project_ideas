from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import DbtCliResource

from . import assets
from .resources.dbt_resource import WEATHER_DBT_PROJECT_DIR, TIMESHEET_DBT_PROJECT_DIR


# Load all assets
dagster_assets = load_assets_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=dagster_assets,
    resources={
        "weather_dbt": DbtCliResource(project_dir=WEATHER_DBT_PROJECT_DIR),
        "timesheet_dbt": DbtCliResource(project_dir=TIMESHEET_DBT_PROJECT_DIR)
    
    }
)