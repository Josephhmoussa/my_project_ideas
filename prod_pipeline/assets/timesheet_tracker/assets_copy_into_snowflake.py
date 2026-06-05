from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult
)

from prod_pipeline.utils.snowflakeclient import SnowflakeClient
from .assets_ingest_bronze_timesheet import ingest_bronze_timesheet, ingest_bronze_lookup

@asset(
    deps=[ingest_bronze_timesheet, ingest_bronze_lookup],
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

    timesheet_status = "success"
    project_codes_status = "success"
    task_codes_status = "success"

    # Timesheets Table
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
        timesheet_status = "failed"
        context.log.error(f"Failed to load timesheet data: {e}")
    
    # Project codes table
    try:
        snowflake_client.execute(
            '''
            copy into project_codes
            from @aws_stage_lookup/project_codes.parquet
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive
            '''
        )
        context.log.info("Successfully loaded timesheet data into bronze table")
    
    except Exception as e:
        project_codes_status = "failed"
        context.log.error(f"Failed to load timesheet data: {e}")
    
    # Task codes table
    try:
        snowflake_client.execute(
            '''
            copy into task_codes
            from @aws_stage_lookup/task_codes.parquet
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive
            '''
        )
        context.log.info("Successfully loaded timesheet data into bronze table")
    
    except Exception as e:
        task_codes_status = "failed"
        context.log.error(f"Failed to load timesheet data: {e}")
    
    finally:
        snowflake_client.close()
        context.log.info("Snowflake connection closed")
    
    return MaterializeResult(
        metadata={
            "timesheet_status": timesheet_status,
            "project_codes_status": project_codes_status,
            "task_codes_status": task_codes_status
        }
    )
