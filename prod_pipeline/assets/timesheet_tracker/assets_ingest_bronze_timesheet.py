from dagster import (
    asset,
    MaterializeResult,
    MetadataValue,
    AssetExecutionContext
)
import polars as pl
from pathlib import Path
from datetime import datetime, UTC

from prod_pipeline.utils.datalakeclient import S3Client

path = Path("prod_pipeline/assets/timesheet_tracker/csv_files/")

@asset(
        group_name="timesheet_pipeline",
        compute_kind="python",
        description="Ingest csv files locally and upload them to S3"
    )
def ingest_bronze_timesheet(context: AssetExecutionContext) -> MaterializeResult:
    '''Ingest csv files with minimal transformations and upload to S3'''

    bucket_name = "timesheets-tracker"
    s3_client = S3Client(bucket_name=bucket_name)

    context.log.info("Extraction started")

    # Loop through csv_files folder, extract data and concat to a single DataFrame
    dfs = []
    for file in path.rglob("*.csv"):
        category = str(file.stem).split("_")[1]
        ingested_at = datetime.now(UTC).strftime("%Y-%m-%d-%H:%M:%S")
        year = str(file.stem).split("_")[-1]
        try:
            df = pl.read_csv(file)
        except Exception as e:
            context.log.error(f"Error reading file {file} to csv: {e}")
            continue

        df = df.with_columns([
            pl.lit(category)
            .cast(pl.Utf8)
            .alias("category"),

            pl.lit(ingested_at)
            .str.to_datetime("%Y-%m-%d-%H:%M:%S")
            .alias("ingested_at"),

            pl.lit(year)
            .cast(pl.Int64)
            .alias("year")
        ])

        dfs.append(df)
    
    df = pl.concat(dfs, how="diagonal_relaxed")

    context.log.info("Dataframe unified successfully")

    # Upload to S3
    file_name = "timesheet_data"
    target_path = (
        f"bronze/"
        f"{file_name}_{ingested_at}.parquet"
    )

    s3_client.upload_dataframe_to_S3(target_path, df)
    context.log.info("Upload to S3 successfull")

    return MaterializeResult(
        metadata={
            "row_number": df.height,
            "preview": MetadataValue.md(df.head().to_pandas().to_markdown())
        }
    )