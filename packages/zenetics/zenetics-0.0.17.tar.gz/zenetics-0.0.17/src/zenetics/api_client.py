import os
from typing import Dict, List

import requests

from zenetics.model import TestCase


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self):

        self.api_key = os.environ.get("ZENETICS_API_KEY")
        self.app_id = os.environ.get("ZENETICS_APP_ID")
        self.host = os.environ.get("ZENETICS_HOST")

        if not self.api_key:
            raise ValueError("ZENETICS_API_KEY environment variable is required")

        if not self.app_id:
            raise ValueError("ZENETICS_APP_ID environment variable is required")

        if not self.host:
            self.host = "https://dev.api.zenetics.io"

    def post(self, body: Dict, api_key: str, app_id: str):
        headers = {
            "Content-Type": "application/json",
            "Zenetics-api-key": api_key,
        }

        response = requests.post(
            self.address + f"/api/v1/apps/{app_id}/sessions", json=body, headers=headers
        )
        if response.status_code != 200:
            raise APIClientError(
                f"Failed to post to {self.address}. Status code {response.status_code}"
            )

    def get(self, endpoint) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "Zenetics-api-key": self.api_key,
        }

        response = requests.get(self.host + endpoint, headers=headers)
        if response.status_code != 200:
            raise APIClientError(
                f"Failed to get from {self.host}. Status code {response.status_code}"
            )
        return response.json()

    def get_testsuites(self, account_id, application_id):
        endpoint = f"/v1/accounts/{account_id}/applications/{application_id}/testsuites"
        response = self.get(endpoint)
        return response

    def get_testcases_by_testsuite(self, account_id, application_id, testsuite_id):
        endpoint = f"/v1/accounts/{account_id}/applications/{application_id}/testsuites/{testsuite_id}/testcases"
        response = self.get(endpoint)
        return response


class APIController:
    def __init__(self):
        self.api_client = APIClient()

    def get_testcases_by_testsuite(self, suite: str) -> List[TestCase]:
        account_id = 42
        application_id = 42
        testsuites = self.api_client.get_testsuites(account_id, application_id)

        testsuite = [ts for ts in testsuites if ts["name"] == suite]

        if not testsuite:
            raise APIClientError(f"Testsuite {suite} not found")

        testsuite_id = testsuite[0]["id"]

        testcases = self.api_client.get_testcases_by_testsuite(
            account_id, application_id, testsuite_id
        )

        testcases = [
            TestCase(
                id=tc["id"],
                name=tc["name"],
                input=tc["input"],
                description=tc.get("description"),
                expected_output=tc.get("expected_output"),
            )
            for tc in testcases
        ]

        return testcases
