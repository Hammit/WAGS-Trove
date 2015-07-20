import requests


class Request:
    API_URL_BASE = 'http://api.trove.nla.gov.au/result'

    def __init__(self, api_key='', zone='newspaper', encoding='json'):
        self.params = {
            'key': api_key,
            'zone': zone,
            'encoding': encoding
        }
        self.response = None

    def get(self, query='11th Battalion', params=None):
        request_params = {}
        if params is not None:
            # Merge supplied params with our request defaults
            request_params = self.params.copy()
            request_params.update(params)
        request_params['q'] = query
        self.response = requests.get(self.API_URL_BASE, params=request_params)
