

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

def ingest_weather_api_bronze(data: dict) -> dict:
    '''Ingest json from API and upload to S3'''

    api = APIClient(base_url)
    data = api.get("archive", params=params)

    return data

print(ingest_weather_api_bronze)