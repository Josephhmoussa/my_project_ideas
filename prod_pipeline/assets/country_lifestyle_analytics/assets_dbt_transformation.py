from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from prod_pipeline.resources.dbt_resource import dbt_project, WeatherDbtTranslator

# DBT Asset
@dbt_assets(
        manifest=dbt_project.manifest_path,
        dagster_dbt_translator=WeatherDbtTranslator()
)
def transform_weather(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()