#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from trove.request import Downloader as TroveDownloader


class TroveRequest:
    API_URL_BASE = 'http://api.trove.nla.gov.au'
    API_URL_BASE_REQUEST = API_URL_BASE + '/result'
    API_ENCODING = 'json'

    def __init__(self, api_key):
        self.params = {
            'key': api_key,
            'encoding': self.API_ENCODING
        }

    def query(self, query, zone='newspaper', params=None):
        request_params = {}
        if params is not None:
            # Merge supplied params with our request defaults
            request_params = self.params.copy()
            request_params.update(params)
        request_params['q'] = query
        request_params['zone'] = zone
        r = requests.get(self.API_URL_BASE_REQUEST, params=request_params)
        response = TroveResponse(r)
        return response

    def get_next_page(self, response):
        r = None  # the response to return
        if response.has_next_page():
            url = response.next_page_url()
            # params = {
            #     'key': self.params['key']
            # }
            # r = requests.get(self.API_URL_BASE + url, params=params)
            url = self.API_URL_BASE + url + '&key=' + self.params['key']
            r = requests.get(url)
            r = TroveResponse(r)
        return r


class TroveResponse:
    def __init__(self, response):
        self.response = response
        self.json = response.json()

    def has_results(self):
        return self.num_records() > 0

    def num_records(self):
        num_results = int(self.json['response']['zone'][0]['records']['n'])
        return num_results

    def has_next_page(self):
        next_page_url = self.next_page_url()
        return (next_page_url is not None)

    def next_page_url(self):
        try:
            next_page_url = self.json['response']['zone'][0]['records']['next']
        except KeyError:
            next_page_url = None

        return next_page_url


if __name__ == "__main__":
    TROVE_URL_BASE = 'http://trove.nla.gov.au'
    TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')

    request = TroveRequest(TROVE_API_KEY)
    request_params = {
        's': 0,
        'n': 75,
        'l-availability': 'y/f',
        'reclevel': 'full',
    }
    response = request.query('11th Battalion date:[1914 TO 1914]', zone='newspaper', params=request_params)
    while response.has_results():
        # Process the results
        print("Processing Records")
        # results = response.results()
        print("{} records of {} starting @ {}".format(
            response.json['response']['zone'][0]['records']['n'],
            response.json['response']['zone'][0]['records']['total'],
            response.json['response']['zone'][0]['records']['s']
        ))
        for article in response.json['response']['zone'][0]['records']['article']:
            image_url = 'http://trove.nla.gov.au/ndp/del/printArticleJpg/{0}/3'.format(article['id'])
            print("Article")
            print("\tURL: %s" % article['url'])
            print("\tPDF: %s" % article['pdf'])
            print("\tImage: %s" % image_url)

            r = requests.get(image_url)
            if r.status_code == requests.codes.ok:
                html_doc = r.text
                soup = BeautifulSoup(html_doc, 'html.parser')
                image = soup.select('img#articleImg')[0]
                TroveDownloader.download_url(TROVE_URL_BASE + image['src'])

        # Get the next page if any
        if not response.has_next_page():
            break
        else:
            print("Getting the next page...")
            response = request.get_next_page(response)
