import boto3
import json
import snowflake.connector

class SnowflakeClient:
    def __init__(self, secret_name, region_name="eu-north-1", database=None, schema=None):
        '''Initialize SnowflakeClient with credentials, database and schema'''

        # Fetch secret from AWS Secrets Manager
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response["SecretString"])

        # Allow overrding database/schema if needed
        self.con = snowflake.connector.connect(
            user=secret["user"],
            password=secret["password"],
            account=secret["account"],
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