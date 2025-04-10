import requests
from urllib.parse import urlencode
import time

class HttpClient:
    """HTTP客户端封装"""
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.session.headers.update(self.headers)

    def get(self, url, params=None):
        """GET请求封装"""
        return self.session.get(f"{self.base_url}{url}", params=params)

    def post(self, url, data=None):
        """POST请求封装"""
        return self.session.post(
            f"{self.base_url}{url}",
            data=urlencode(data) if data else None,
            allow_redirects=False
        )