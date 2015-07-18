#!/usr/bin/env python3


import os
import requests

TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')


class TroveRequest:
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


if __name__ == "__main__":
    trove = TroveRequest(api_key=TROVE_API_KEY)
    trove_query_params = {
        's': 0,               # start
        'n': 50,              # num of results
        'l-illustrated': 'Y'
    }
    trove.get(query='11th Battalion date:[1914 TO 1921]', params=trove_query_params)
    print("Request URL: %s" % trove.response.url)
    if trove.response.status_code != requests.codes.ok:
        print("Error: Problem processing request")
    else:
        # print("Response: %s" % trove.response.text)
        response = trove.response.json()
        # print("Response Records: %s" % response['response'])
        print("%s Records" % response['response']['zone'][0]['records']['total'])
        for article in response['response']['zone'][0]['article']:
            print("Article URL: %s" % article['url'])
