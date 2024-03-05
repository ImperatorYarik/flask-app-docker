
import unittest
from unittest.mock import patch, MagicMock

import requests

from handlers.pull_requests import get_pull_requests, BASE_URL


BASE_URL = 'https://api.github.com/repos/boto/boto3/pulls'


def get_pull_requests(state):
    params = {'state': state, 'per_page': 100}

    response = requests.get(BASE_URL, params)
    if response.status_code == 200:
        pull_requests_data = response.json()
        pull_requests_info = []
        for pr in pull_requests_data:
            pull_request_info = {
                'title': pr['title'],
                'num': pr['number'],
                'link': pr['html_url']
            }
            pull_requests_info.append(pull_request_info)
        return pull_requests_info
    else:
        return []


class TestGetPullRequests(unittest.TestCase):

    def test_successful_response(self):
        # Mock the requests.get method to return a successful response
        mocked_response = unittest.mock.MagicMock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = [
            {'title': 'PR Title 1', 'number': 123, 'html_url': 'https://github.com/pull/123'},
            {'title': 'PR Title 2', 'number': 456, 'html_url': 'https://github.com/pull/456'},
        ]
        with unittest.mock.patch('requests.get', return_value=mocked_response):
            pull_requests = get_pull_requests('open')

        self.assertEqual(len(pull_requests), 2)
        self.assertEqual(pull_requests[0]['title'], 'PR Title 1')
        self.assertEqual(pull_requests[0]['num'], 123)
        self.assertEqual(pull_requests[0]['link'], 'https://github.com/pull/123')

    def test_unsuccessful_response(self):
        # Mock the requests.get method to return an unsuccessful response
        mocked_response = unittest.mock.MagicMock()
        mocked_response.status_code = 404
        with unittest.mock.patch('requests.get', return_value=mocked_response):
            pull_requests = get_pull_requests('open')

        self.assertEqual(pull_requests, [])


if __name__ == '__main__':
    unittest.main()

