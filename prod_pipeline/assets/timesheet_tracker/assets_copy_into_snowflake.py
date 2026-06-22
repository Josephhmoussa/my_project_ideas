from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult
)

from prod_pipeline.utils.snowflakeclient import SnowflakeClient
from .assets_ingest_bronze_timesheet import ingest_bronze_timesheet, ingest_bronze_lookup

@asset(
        key = ["bronze", "timesheets"],
        deps=[ingest_bronze_timesheet],
        group_name="timesheet_pipeline",
        compute_kind="python",
        description="Copy raw timesheets data into bronze layer in Snowflake"
)

def copy_timesheets_into_snowflake(context: AssetExecutionContext) -> MaterializeResult:
    '''Copy raw timesheet data into Snowflake bronze layer'''

    snowflake_client = SnowflakeClient(
        creds_secret_name="prod/snowflake/credentials",
        key_secret_name="prod/snowflake/private_key",
        database="timesheet_pipeline",
        schema="bronze"
    )

    timesheet_status = "success"

    # Timesheets Table
    try:
        snowflake_client.execute("TRUNCATE TABLE timesheets")
        snowflake_client.execute(
            '''
            copy into timesheets
            from @aws_stage_timesheets
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive
            force = TRUE;
            '''
        )
        context.log.info("Successfully loaded timesheet data into bronze table")
    
    except Exception as e:
        timesheet_status = "failed"
        context.log.error(f"Failed to load timesheet data: {e}")
    
    finally:
        snowflake_client.close()
        context.log.info("Snowflake connection closed")
    
    return MaterializeResult(
        metadata={
            "timesheet_status": timesheet_status
        }
    )


@asset(
        key = ["bronze", "project_codes"],
        deps=[ingest_bronze_lookup],
        group_name="timesheet_pipeline",
        compute_kind="python",
        description="Copy raw project codes data into bronze layer in Snowflake"
)

def copy_project_codes_into_snowflake(context: AssetExecutionContext) -> MaterializeResult:
    '''Copy raw project codes data into Snowflake bronze layer'''

    snowflake_client = SnowflakeClient(
        creds_secret_name="prod/snowflake/credentials",
        key_secret_name="prod/snowflake/private_key",
        database="timesheet_pipeline",
        schema="bronze"
    )

    project_codes_status = "success"
    
    # Project codes table
    try:
        snowflake_client.execute("TRUNCATE TABLE project_codes")
        snowflake_client.execute(
            '''
            copy into project_codes
            from @aws_stage_lookup/project_codes.parquet
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive
            force = TRUE;
            '''
        )
        context.log.info("Successfully loaded project codes data into bronze table")
    
    except Exception as e:
        project_codes_status = "failed"
        context.log.error(f"Failed to load project codes data: {e}")
    
    finally:
        snowflake_client.close()
        context.log.info("Snowflake connection closed")
    
    return MaterializeResult(
        metadata={
            "project_codes_status": project_codes_status
        }
    )


@asset(
        key = ["bronze", "task_codes"],
        deps=[ingest_bronze_lookup],
        group_name="timesheet_pipeline",
        compute_kind="python",
        description="Copy raw task codes data into bronze layer in Snowflake"
)

def copy_task_codes_into_snowflake(context: AssetExecutionContext) -> MaterializeResult:
    '''Copy raw task codes data into Snowflake bronze layer'''

    snowflake_client = SnowflakeClient(
        creds_secret_name="prod/snowflake/credentials",
        key_secret_name="prod/snowflake/private_key",
        database="timesheet_pipeline",
        schema="bronze"
    )

    task_codes_status = "success"
    
    # Task codes table
    try:
        snowflake_client.execute("TRUNCATE TABLE task_codes")
        snowflake_client.execute(
            '''
            copy into task_codes
            from @aws_stage_lookup/task_codes.parquet
            file_format = (format_name = ff_parquet)
            match_by_column_name = case_insensitive
            force = TRUE;
            '''
        )
        context.log.info("Successfully loaded task codes data into bronze table")
    
    except Exception as e:
        task_codes_status = "failed"
        context.log.error(f"Failed to load task codes data: {e}")
    
    finally:
        snowflake_client.close()
        context.log.info("Snowflake connection closed")
    
    return MaterializeResult(
        metadata={
            "task_codes_status": task_codes_status
        }
    )
