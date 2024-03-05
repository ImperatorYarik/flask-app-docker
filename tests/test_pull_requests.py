
import unittest
from unittest.mock import patch, MagicMock

import requests

from handlers.pull_requests import get_pull_requests, BASE_URL


class TestOpenPullRequests(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_pull_requests(self, get_mock):
        """Test open pull requests"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'number': 4010,
                'title': 'DynamoDB: Add support for…items for boto3 resource',
                'html_url': 'https://github.com/boto/boto3/pull/4010'
            }
        ]

        get_mock.return_value = mock_response

        expected_res = [
            {
                'num': 4010,
                'title': 'DynamoDB: Add support for…items for boto3 resource',
                'link': 'https://github.com/boto/boto3/pull/4010'
            }
        ]
        res = get_pull_requests('open')
        self.assertEqual(res, expected_res)


class TestClosedPullRequests(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_pull_requests(self, get_mock):
        """Test closed pull requests"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'number': 3998,
                'title': 'Minor GitHub workflow changes',
                'html_url': 'https://github.com/boto/boto3/pull/3998'
            }
        ]

        get_mock.return_value = mock_response

        expected_res = [
            {
                'num': 3998,
                'title': 'Minor GitHub workflow changes',
                'link': 'https://github.com/boto/boto3/pull/3998'
            }
        ]
        res = get_pull_requests('closed')
        self.assertEqual(res, expected_res)

class TestPullRequestsFailure(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_api_failure(self, get_mock):
        """Test API failure scenarios"""
        # Simulate a 404 Not Found error
        mock_response = MagicMock()
        mock_response.status_code = 404
        get_mock.return_value = mock_response

        result = get_pull_requests('open')
        self.assertEqual(result, [], "Should return an empty list on API failure")

class TestEmptyPullRequests(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_empty_pull_requests(self, get_mock):
        """Test receiving an empty list of pull requests"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        get_mock.return_value = mock_response

        result = get_pull_requests('open')
        self.assertEqual(result, [], "Should return an empty list when no pull requests are found")


class TestBaseUrlUsage(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_base_url_usage(self, mock_get):
        """Test that the correct BASE_URL is used in API requests."""
        get_pull_requests('open')

        self.assertTrue(mock_get.called, "requests.get should be called.")

        called_url = mock_get.call_args[0][0]

        self.assertEqual(called_url, BASE_URL, f"Expected BASE_URL '{BASE_URL}', but got '{called_url}'.")


class TestParams(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_params(self, mock_get):
        """Test that the correct parameters are passed in API requests."""
        get_pull_requests('open')

        self.assertTrue(mock_get.called, "requests.get should be called.")

        called_args, _ = mock_get.call_args

        self.assertIn('state', called_args[1], "'state' parameter should be included in the call to requests.get.")
        self.assertIn('per_page', called_args[1],
                      "'per_page' parameter should be included in the call to requests.get.")

        state_param = called_args[1]['state']
        per_page_param = called_args[1]['per_page']

        self.assertEqual(state_param, 'open', "Expected 'state' parameter to be 'open'.")
        self.assertEqual(per_page_param, 100, "Expected 'per_page' parameter to be 100.")

class TestErrorHandling(unittest.TestCase):
    @patch('handlers.pull_requests.requests.get')
    def test_api_failure(self, mock_get):
        """Test handling of API failure."""
        # Simulate API failure (e.g., 404 Not Found)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Ensure an empty list is returned on API failure
        result = get_pull_requests('open')
        self.assertEqual(result, [], "Should return an empty list on API failure.")

    @patch('handlers.pull_requests.requests.get')
    def test_empty_response(self, mock_get):
        """Test handling of empty API response."""
        # Simulate an empty API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_get.return_value = mock_response

        # Ensure an empty list is returned when API response is empty
        result = get_pull_requests('open')
        self.assertEqual(result, [], "Should return an empty list when API response is empty.")


if __name__ == '__main__':
    unittest.main()

