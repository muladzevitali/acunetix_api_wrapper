import os
from typing import Tuple

import requests

from src.config import acunetix_api_config


class SearchEngineBaseApi:
    accepted_status_codes = [200, 201, 204]

    def __init__(self, api_token=acunetix_api_config.api_key):
        self.token = api_token
        self.base_url = acunetix_api_config.api_url
        self.headers = {'X-Auth': api_token}

    def get(self, endpoint, **kwargs) -> Tuple[requests.Response, bool]:
        """
        Get request wrapper for api
        """
        url = os.path.join(self.base_url, endpoint)
        response = requests.get(url, headers=self.headers, verify=False, **kwargs)

        return response, True if response.status_code == 200 else False

    def post(self, endpoint, **kwargs) -> Tuple[requests.Response, bool]:
        """
        Post request wrapper for api
        """
        headers = {**self.headers, 'Content-Type': 'application/json'}
        url = os.path.join(self.base_url, endpoint)
        response = requests.post(url, headers=headers, verify=False, **kwargs)

        return response, response.status_code in self.accepted_status_codes

    def patch(self, endpoint: str, **kwargs):
        """
        Patch request wrapper for api
        """
        headers = {**self.headers, 'Content-Type': 'application/json'}
        url = os.path.join(self.base_url, endpoint)
        response = requests.patch(url, headers=headers, verify=False, **kwargs)

        return response, response.status_code in self.accepted_status_codes
