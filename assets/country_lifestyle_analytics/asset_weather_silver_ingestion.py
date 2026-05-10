import polars as pl
import io

from utils.datalakeclient import S3Client

bucket_name = "country-lifestyle-analytics"
datalake_client = S3Client(bucket_name=bucket_name)

def ingest_weather_api_silver() -> pl.DataFrame:
    '''Ingest bronze data normalize and load to silver'''

    bronze_folder_path = f"bronze/weather"

    # Get bronze files and load to df
    paths = datalake_client.get_paths_from_folder(bronze_folder_path)

    dfs = []
    for path in paths:
        data = datalake_client.get_nested_json(path)

        df = pl.DataFrame(data["daily"])

        df = df.with_columns([
            pl.lit(data["latitude"]).alias("latitude"),
            pl.lit(data["longitude"]).alias("longitude")
        ])

        dfs.append(df)

    return dfs

print(ingest_weather_api_silver())