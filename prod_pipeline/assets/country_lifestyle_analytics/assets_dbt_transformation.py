from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from prod_pipeline.resources.dbt_resource import weather_dbt_project, WeatherDbtTranslator

# DBT Asset
@dbt_assets(
        manifest=weather_dbt_project.manifest_path,
        dagster_dbt_translator=WeatherDbtTranslator()
)
def transform_weather(context: AssetExecutionContext, weather_dbt: DbtCliResource):
    yield from weather_dbt.cli(["build"], context=context).stream()