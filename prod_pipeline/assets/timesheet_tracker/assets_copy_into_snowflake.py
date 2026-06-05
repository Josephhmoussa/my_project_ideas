from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult
)

from prod_pipeline.utils.snowflakeclient import SnowflakeClient
from .assets_ingest_bronze_timesheet import ingest_bronze_timesheet

@asset(
    deps=[ingest_bronze_timesheet],
    group_name="timesheet_pipeline",
    compute_kind="python",
    description="Copy raw data into bronze layer in Snowflake"
)

def copy_into_snowflake(context: AssetExecutionContext) -> MaterializeResult:
    '''Copy raw data into Snowflake bronze layer'''

    snowflake_client = SnowflakeClient(
        creds_secret_name="prod/snowflake/credentials",
        key_secret_name="prod/snowflake/private_key",
        database="timesheet_pipeline",
        schema="bronze"
    )
    status = "success"
    try:
        snowflake_client.execute(
            '''
            copy into timesheets
            from @aws_stage_timesheets
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive;
            '''
        )
        context.log.info("Successfully loaded timesheet data into bronze table")
    
    except Exception as e:
        status = "failed"
        context.log.error(f"Failed to load timesheet data: {e}")
    
    finally:
        snowflake_client.close()
        context.log.info("Snowflake connection closed")
    
    return MaterializeResult(
        metadata={
            "status": status
        }
    )
