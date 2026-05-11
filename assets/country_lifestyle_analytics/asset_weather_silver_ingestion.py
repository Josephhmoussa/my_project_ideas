import polars as pl
import logging

from utils.datalakeclient import S3Client

logger = logging.getLogger(__name__)

bucket_name = "country-lifestyle-analytics"
datalake_client = S3Client(bucket_name=bucket_name)

def ingest_weather_api_silver() -> pl.DataFrame:
    '''Ingest bronze data normalize and load to silver'''

    logger.info("Starting Silver Layer ingestion")

    bronze_folder_path = f"bronze/weather"

    # Get bronze files
    paths = datalake_client.get_paths_from_folder(bronze_folder_path)

    # Load to Dataframes and concat
    dfs = []
    for path in paths:
        data = datalake_client.get_nested_json(path)

        df = pl.DataFrame(data["daily"])

        df = df.with_columns([
            pl.lit(data["latitude"]).alias("latitude"),
            pl.lit(data["longitude"]).alias("longitude")
        ])

        dfs.append(df)

    if not dfs:
        logger.warning("No data found in bronze layer")
        return pl.DataFrame()

    df = pl.concat(dfs)

    # Normalize columns
    df = df.rename(
        lambda col: (
            col.strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
        )
    )

    # Enforce schema
    df = df.with_columns([
        pl.col("time")
        .str
        .to_date("%Y-%m-%d")
        .alias("date"),

        pl.col("temperature_2m_max")
        .cast(pl.Float64),

        pl.col("sunshine_duration")
        .cast(pl.Float64),

        pl.col("precipitation_sum")
        .cast(pl.Float64),

        pl.col("latitude")
        .cast(pl.Float64),

        pl.col("longitude")
        .cast(pl.Float64)
    ]).drop("time")

    # Save to parquet and upload to S3
    target_path = (
        f"silver/"
        f"weather/"
        f"weather.parquet"
    )

    datalake_client.upload_dataframe_to_S3(target_path, df)
    logger.info(f"Silver data uploaded to {target_path}")

    return df

print(ingest_weather_api_silver())