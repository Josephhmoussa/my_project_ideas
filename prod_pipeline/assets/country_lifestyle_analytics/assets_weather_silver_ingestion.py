# from dagster import (
#     asset,
#     AssetExecutionContext,
#     MaterializeResult,
#     MetadataValue
# )

# import polars as pl
# from .assets_weather_bronze_ingestion import ingest_weather_api_bronze

# from prod_pipeline.utils.datalakeclient import S3Client


# bucket_name = "country-lifestyle-analytics"

# @asset(
#         group_name="country_lifestyle_analytics",
#         compute_kind="python",
#         deps=[ingest_weather_api_bronze],
#         description="Ingests bronze data and apply transformation"
# )
# def ingest_weather_api_silver(context:AssetExecutionContext) -> MaterializeResult:
#     '''Ingest bronze data normalize and load to silver'''

#     context.log.info("Starting Silver Layer ingestion")

#     bronze_folder_path = f"bronze/weather"

#     datalake_client = S3Client(bucket_name=bucket_name)

#     # Get bronze files
#     paths = datalake_client.get_paths_from_folder(bronze_folder_path)

#     # Load to Dataframes and concat
#     dfs = []
#     for path in paths:

#         if path.endswith(".json"):

#             data = datalake_client.get_nested_json(path)

#             df = pl.DataFrame(data["data"]["daily"])

#             df = df.with_columns([
#                 pl.lit(data["data"]["latitude"]).alias("latitude"),
#                 pl.lit(data["data"]["longitude"]).alias("longitude"),
#                 pl.lit(data["city"]).alias("city"),
#                 pl.lit(data["ingested_at"]).alias("ingested_at")
#             ])

#             dfs.append(df)

#     if not dfs:
#         context.log.warning("No data found in bronze layer")
#         return MaterializeResult(
#             metadata={
#                 "row_count": 0
#             }
#         )

#     df = pl.concat(dfs)

#     # Normalize columns
#     df = df.rename(
#         lambda col: (
#             col.strip()
#                 .lower()
#                 .replace(" ", "_")
#                 .replace("-", "_")
#         )
#     )

#     # Enforce schema
#     df = df.with_columns([
#         pl.col("time")
#         .str
#         .to_date()
#         .alias("date"),

#         pl.col("temperature_2m_max")
#         .cast(pl.Float64),

#         pl.col("sunshine_duration")
#         .cast(pl.Float64),

#         pl.col("precipitation_sum")
#         .cast(pl.Float64),

#         pl.col("latitude")
#         .cast(pl.Float64),

#         pl.col("longitude")
#         .cast(pl.Float64),

#         pl.col("ingested_at")
#         .cast(pl.Datetime),

#         pl.col("city")
#         .cast(pl.Utf8)

#     ]).drop("time")

#     # Deduplication (keep latest ingestion per city/date)
#     df = (
#         df
#         .sort("ingested_at")
#         .unique(
#             subset=["city", "date"],
#             keep="last"
#         )
#     )

#     # Save to parquet and upload to S3
#     target_path = (
#         f"silver/"
#         f"weather/"
#         f"weather.parquet"
#     )

#     datalake_client.upload_dataframe_to_S3(target_path, df)
#     context.log.info(f"Silver data uploaded to {target_path}")

#     return MaterializeResult(
#         metadata={
#             "row_number": df.height,
#             "preview": MetadataValue.md(df.head().to_pandas().to_markdown())
#         }
#     )