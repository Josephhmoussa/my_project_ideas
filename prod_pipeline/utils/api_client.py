import requests
from dagster import get_dagster_logger

dagster_logger = get_dagster_logger()


class APIClient:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = 30):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
    
    def get(self, endpoint: str, params: dict = None) -> dict:
        '''Get response from API using endpoint and params'''

        try:

            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            dagster_logger.warning(f"Get request failed for endpoint {endpoint}: {e}")
            raise Exception(f"Get request failed for endpoint {endpoint}: {e}")

    
    def post(self, endpoint: str, data: dict = None) -> dict:
        ''' Post response using endpoint and data'''

        try:

            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            dagster_logger.warning(f"Post request failed for endpoint {endpoint}: {e}")
            raise Exception(f"Post request failed for endpoint {endpoint}: {e}")