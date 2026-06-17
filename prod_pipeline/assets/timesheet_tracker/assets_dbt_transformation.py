from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from prod_pipeline.resources.dbt_resource import timesheet_dbt_project, TimesheetDbtTranslator

# DBT Asset
@dbt_assets(
    manifest=timesheet_dbt_project.manifest_path,
    dagster_dbt_translator=TimesheetDbtTranslator()
)
def transform_timesheet(context: AssetExecutionContext, timesheet_dbt: DbtCliResource):
    yield from timesheet_dbt.cli(["build"], context=context).stream()