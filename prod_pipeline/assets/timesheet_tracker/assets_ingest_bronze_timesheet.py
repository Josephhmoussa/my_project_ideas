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

    bucket_name = ""
    s3_client = S3Client(bucket_name=bucket_name)

    context.log.info("Extraction started")

    # Loop through csv_files folder, extract data and concat to a single DataFrame
    dfs = []
    for file in path.rglob("*.csv"):
        category = str(file).split("/")[-1].split("_")[1]
        ingested_at = datetime.now(UTC).strftime("%Y-%m-%d-%H:%M:%S")
        df = pl.read_csv(file)

        df = df.with_columns([
            pl.lit(category)
            .cast(pl.Utf8)
            .alias("category"),

            pl.lit(ingested_at)
            .str.to_datetime("%Y-%m-%d-%H:%M:%S")
            .alias("ingested_at")
        ])

        dfs.append(df)
    
    df = pl.concat(dfs, how="diagonal_relaxed")

    # Upload to S3
    target_path = ""

    return df

if __name__ == "__main__":
    result = ingest_bronze_timesheet(path)

    print(result)