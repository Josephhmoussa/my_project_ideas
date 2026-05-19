from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue
)

import polars as pl
import json
from datetime import datetime, UTC

from prod_pipeline.utils.datalakeclient import S3Client
from prod_pipeline.utils.api_client import APIClient

csv_path = "prod_pipeline/assets/country_lifestyle_analytics/worldcities.csv"
base_url = "https://archive-api.open-meteo.com/v1/"

bucket_name = "country-lifestyle-analytics"
datalake_client = S3Client(bucket_name=bucket_name)

@asset(group_name="country_lifestyle_analytics",
       compute_kind= "csv",
       description="upload lookup table to S3")

def upload_lookup_table(context: AssetExecutionContext) -> MaterializeResult:
    '''Upload CSV lookup table to S3'''
    file_name = "worldcities.csv"
    target_path = f"bronze/weather/lookup/{file_name}"
    
    with open(csv_path, "rb") as f:
        datalake_client.upload_bytes(
            target_path,
            f.read()
        )
    
    context.log.info(f"Uploaded {file_name} to {target_path}")
    
    return MaterializeResult(
        metadata={
            "s3_path": target_path,
            "file_name": "worldcities.csv"
        }
    )

@asset(group_name="country_lifestyle_analytics",
       compute_kind="bronze",
       deps=[upload_lookup_table],
       description="Load csv lookup table + ingest weather API and load to bronze S3")

def ingest_weather_api_bronze(context: AssetExecutionContext) -> MaterializeResult:
    '''Ingest json from API + load csv world cities lookup table and upload to S3'''

    context.log.info("Starting weather API ingestion")
    file_name = "worldcities.csv"
    CSV_PATH = f"bronze/weather/lookup/{file_name}"

    schema_overrides = {
        "population": pl.Float64
    }

    # Load lookup table from S3
    df = datalake_client.get_csv_to_dataframe(CSV_PATH, schema_overrides).head(3)

    # API call
    api = APIClient(base_url)

    results = []
    for row in df.iter_rows(named=True):
        lat = row["lat"]
        lon = row["lng"]
        city = row["city_ascii"]

        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2026-04-17",
            "end_date": "2026-05-01",
            "daily": ["temperature_2m_max", "sunshine_duration", "precipitation_sum"]
        }

        # Get data
        data = api.get("archive", params=params)

        # Wrap Metadata
        wrapped_data = {
            "city": city,
            "ingested_at": datetime.now(UTC).isoformat(),
            "source": "open_meteo",
            "data": data
        }

        # Convert dict -> json -> bytes
        data_bytes = json.dumps(wrapped_data, separators=(",", ":")).encode("utf-8")

        # Timestamp
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Save to S3
        target_path = (
            f"bronze/weather/"
            f"city={city}/"
            f"weather_{timestamp}.json"
        )
        datalake_client.upload_bytes(target_path=target_path, data=data_bytes)

        context.log.info(f"Uploaded weather data for {city} to {target_path} ")

        results.append(wrapped_data)

    return MaterializeResult(
        metadata={
            "number_cities": len(results),
            "api_preview": MetadataValue.json(results[:1]),
            "lookup_nbr_rows": df.height,
            "lookup_preview": MetadataValue.md(df.head().to_pandas().to_markdown())
        }
    )