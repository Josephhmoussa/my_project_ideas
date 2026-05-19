import boto3
from botocore.config import Config
import io
import polars as pl
import json


class S3Client:
    def __init__(self, bucket_name: str):
        '''Initialize S3Client with credentials and bucket_name '''

        self.s3 = boto3.client(
            "s3",
            config = Config(
                connect_timeout=60,
                read_timeout=600
            )
        )
        self.bucket_name = bucket_name
    
    def get_paths_from_folder(self, folder_name: str) -> set[str]:
        '''Return object paths from an S3 prefix'''

        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=folder_name
        )

        contents = response.get("Contents", [])

        full_paths = {obj["Key"] for obj in contents if not obj["Key"].endswith("/")}
        return full_paths
    
    def download_file(self, source_path: str):
        '''Download file from S3'''

        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=source_path
        )
        return response["Body"].read()
    
    def upload_bytes(self, target_path: str, data: bytes):
        '''Upload file to S3'''

        return self.s3.put_object(
            Bucket=self.bucket_name,
            Key=target_path,
            Body=data
        )

    def get_csv_to_dataframe(self, source_path: str, schema_overrides: dict) -> pl.DataFrame:
        '''Get CSV file from source path and load it as Dataframe'''
    
        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=source_path
        )

        content = response["Body"].read()
        df = pl.read_csv(io.BytesIO(content), schema_overrides=schema_overrides)
        return df
    
    def get_parquet_to_dataframe(self, source_path: str) -> pl.DataFrame:
        '''Get parquet file from source path and load it to a polars Dataframe'''

        response = self.s3.get_object(
            Bucket = self.bucket_name,
            Key = source_path
        )

        content = response["Body"].read()
        df = pl.read_parquet(io.BytesIO(content))
        return df
    
    def get_flat_json_to_dataframe(self, source_path: str) -> pl.DataFrame:
        '''Get json from S3 and load it to a polars Dataframe'''

        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=source_path
        )

        content = response["Body"].read()
        df = pl.read_json(io.BytesIO(content))
        return df
    
    def get_nested_json(self, source_path: str) -> dict:
        '''Get JSON file from S3 and load it as dict'''

        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=source_path
        )

        content = response["Body"].read()

        # Bytes -> dict
        data = json.loads(content.decode("utf-8"))

        return data
    
    def upload_dataframe_to_S3(self, target_path: str, df: pl.DataFrame):
        '''Upload Dataframe to specific target path to S3'''

        # Empty bytes file
        buffer = io.BytesIO()

        # Write df to parquet
        df.write_parquet(buffer)

        # Reset cursor to the begining
        buffer.seek(0)

        # Upload to S3
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=target_path,
            Body=buffer.getvalue()
        )