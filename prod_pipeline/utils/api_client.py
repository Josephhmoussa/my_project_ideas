import requests


class APIClient:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = 30):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
    
    def get(self, endpoint: str, params: dict = None) -> dict:
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: dict = None) -> dict:
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()