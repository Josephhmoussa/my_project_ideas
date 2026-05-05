import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv

load_dotenv()


class S3Client:
    def __init__(self, bucket_name):
        '''Initialize S3Client with credentials and container_name '''
        self.service_client = boto3.client(
            "s3",
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name = os.getenv("AWS_DEFAULT_REGION"),

            config = Config(
                connect_timeout=60,
                read_timeout=600
            )
        )
        self.bucket_name = bucket_name