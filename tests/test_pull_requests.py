
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




if __name__ == '__main__':
    unittest.main()

