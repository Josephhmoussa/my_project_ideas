import polars as pl
import json
from datetime import datetime, UTC
import logging

from utils.datalakeclient import S3Client
from utils.api_client import APIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

csv_path = "assets/country_lifestyle_analytics/worldcities.csv"
base_url = "https://archive-api.open-meteo.com/v1/"
bucket_name = "country-lifestyle-analytics"
datalake_client = S3Client(bucket_name=bucket_name)

def lookup_worldcities(csv_path: str) -> pl.DataFrame:
    '''Get CSV and load it into polars Dataframe'''

    df = pl.read_csv(csv_path, schema_overrides={"population": pl.Float64})
    return df.head(3)


def ingest_weather_api_bronze(url: str, df: pl.DataFrame) -> list[dict]:
    '''Ingest json from API and upload to S3'''

    logger.info("Starting weather API ingestion")
    # API call
    api = APIClient(url)

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

        # Convert dict -> json -> bytes
        data_bytes = json.dumps(data).encode("utf-8")

        # Timestamp
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Save to S3
        target_path = (
            f"bronze/weather/"
            f"city={city}/"
            f"weather_{timestamp}.json"
        )
        datalake_client.upload_bytes(target_path=target_path, data=data_bytes)

        logger.info(f"Uploaded weather data for {city} to {target_path} ")

        results.append(data)

    return results