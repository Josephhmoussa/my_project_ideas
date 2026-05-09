import polars as pl
import json
from datetime import datetime, UTC

from utils.datalakeclient import S3Client
from utils.api_client import APIClient

base_url = "https://archive-api.open-meteo.com/v1/"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "start_date": "2026-04-17",
    "end_date": "2026-05-01",
    "daily": ["temperature_2m_max", "sunshine_duration", "precipitation_sum"]
}
bucket_name = "country-lifestyle-analytics"
datalake_client = S3Client(bucket_name=bucket_name)

def ingest_weather_api_bronze(url: str, params: dict) -> dict:
    '''Ingest json from API and upload to S3'''

    # Read data from api
    api = APIClient(url)
    data = api.get("archive", params=params)

    # Convert dict -> json -> bytes
    data_bytes = json.dumps(data).encode("utf-8")

    # Timestamp
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    # Save to S3
    target_path = (f"bronze/weather/weather_data_{timestamp}.json")
    datalake_client.upload_bytes(target_path=target_path, data=data_bytes)

    return data

data = ingest_weather_api_bronze(base_url, params)
pretty_data = json.dumps(data, indent=4)
print(pretty_data)