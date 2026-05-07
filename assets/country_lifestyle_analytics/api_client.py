import requests


class APIclient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json"
        })

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })