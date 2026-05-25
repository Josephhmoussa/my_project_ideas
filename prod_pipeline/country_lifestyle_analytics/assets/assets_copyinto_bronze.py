from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult
)

from utils.snowflakeclient import SnowflakeClient
from .assets_weather_bronze_ingestion import ingest_weather_api_bronze


@asset(
    deps=[ingest_weather_api_bronze],
    group_name="country_lifestyle_analytics",
    compute_kind="python",
    description="Copy raw data in Snowflake from stage to bronze"
)

def load_weather_to_snowflake(context: AssetExecutionContext) -> MaterializeResult:
    '''Copy raw data from Snowflake stage in to bronze layer'''

    snowflake_client = SnowflakeClient("prod/snowflake/credentials", database="COUNTRY_LIFESTYLE_ANALYTICS", schema="bronze")
    status = "success"
    try:
        snowflake_client.execute(
            '''
            COPY INTO weather_raw (raw)
            FROM @aws_stage
            FILE_FORMAT = (TYPE = 'JSON')
            PATTERN = '.*weather_.*\\.json';
            '''
        )
        context.log.info(f"Successfully loaded weather data to bronze")
    
    except Exception as e:
        status = "failed"
        context.log.error(f"Failed to load weather data: {e}")

    finally:
        snowflake_client.close()
        context.log.info(f"Snowflake connnection closed")
    
    return MaterializeResult(
        metadata={
            "status": status
        }
    )