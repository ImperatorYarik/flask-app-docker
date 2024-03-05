
import unittest
from unittest.mock import patch

from handlers.pull_requests import get_pull_requests

BASE_URL = 'https://api.github.com/repos/boto/boto3/pulls'



class TestGetPullRequests(unittest.TestCase):

    @unittest.mock.patch('requests.get')
    def test_successful_response(self, mock_get):
        # Mock successful response with data
        mocked_response = unittest.mock.MagicMock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = [{'title': 'Test PR', 'number': 123, 'html_url': 'https://example.com/pull/123'}]
        mock_get.return_value = mocked_response

        pull_requests = get_pull_requests('open')

        self.assertEqual(len(pull_requests), 1)
        self.assertEqual(pull_requests[0]['title'], 'Test PR')
        self.assertEqual(pull_requests[0]['num'], 123)
        self.assertEqual(pull_requests[0]['link'], 'https://example.com/pull/123')

    @unittest.mock.patch('requests.get')
    def test_unsuccessful_response(self, mock_get):
        # Mock unsuccessful response
        mocked_response = unittest.mock.MagicMock()
        mocked_response.status_code = 404
        mock_get.return_value = mocked_response

        pull_requests = get_pull_requests('open')

        self.assertEqual(pull_requests, [])

    @unittest.mock.patch('requests.get')
    def test_empty_response(self, mock_get):
        # Mock successful response with empty data
        mocked_response = unittest.mock.MagicMock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = []
        mock_get.return_value = mocked_response

        pull_requests = get_pull_requests('open')

        self.assertEqual(pull_requests, [])

    @unittest.mock.patch('requests.get')
    def test_exception_raised(self, mock_get):
        # Mock exception during request
        mock_get.side_effect = Exception('Mocked Exception')

        with self.assertRaises(Exception):
            get_pull_requests('open')




if __name__ == '__main__':
    unittest.main()

