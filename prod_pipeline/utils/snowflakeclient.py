import boto3
import json
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class SnowflakeClient:
    def __init__(self, creds_secret_name, key_secret_name, region_name="eu-north-1", database=None, schema=None):
        '''Initialize SnowflakeClient with credentials, database and schema'''

        # Fetch secret from AWS Secrets Manager
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=creds_secret_name)
        secret = json.loads(get_secret_value_response["SecretString"])

        # Fetch private key from AWS Secrets Manager
        key_response = client.get_secret_value(SecretId=key_secret_name)
        pem_key = key_response['SecretString'].encode()

        # Convert PEM to DER format (required by Snowflake connector)
        private_key = serialization.load_pem_private_key(
            pem_key, password=None, backend=default_backend()
        ).private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Allow overrding database/schema if needed
        self.con = snowflake.connector.connect(
            user=secret["user"],
            account=secret["account"],
            private_key = private_key,
            warehouse=secret["warehouse"],
            database=database or secret["database"],
            schema=schema or secret["schema"],
            role=secret["role"]
        )
    
    def execute(self, sql):
        '''Execute sql commands based on Snowflake connection'''
        cs = self.con.cursor()
        try:
            cs.execute(sql)
            return cs.fetchall()
        finally:
            cs.close()
    
    def close(self):
        '''Close Snowflake connection'''
        self.con.close()