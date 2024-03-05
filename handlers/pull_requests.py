
import requests

BASE_URL = 'https://api.github.com/repos/boto/boto3/pulls'

def get_pull_requests(state):
    params = {'state': state, 'per_page': 100}

    # Write your code here
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


