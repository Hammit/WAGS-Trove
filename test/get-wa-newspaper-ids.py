#!/usr/bin/env python3

import os
import requests

TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')
TROVE_API_URL_BASE = 'http://api.trove.nla.gov.au/newspaper/titles'

def newspaper_ids(response):
    ids = []
    newspapers = response['response']['records']['newspaper']
    for newspaper in newspapers:
        ids.append(newspaper['id'])
    return ids

def newspaper_url_params(newspaper_ids):
    url_params = ""
    for newspaper_id in newspaper_ids:
        url_params += "l-title={0}&".format(newspaper_id)
    url_params.rstrip('&')
    return url_params

if __name__ == "__main__":
    state  = 'wa'
    api_encoding = 'json'
    params = {
        'key': TROVE_API_KEY,
        'state': state,
        'encoding': api_encoding
    }

    r = requests.get(TROVE_API_URL_BASE, params=params)
    print("Request URL: %s" % r.url)
    if r.status_code != requests.codes.ok:
        print("Error: Problem processing request")
    else:
        # print("Response: %s" % r.text)
        response = r.json()
        # print("Response Records: %s" % response['response']['records']['newspaper'])
        newspapers = newspaper_ids(response)
        # print("Newspaper Ids: %s" % newspapers)
        url_params = newspaper_url_params(newspapers)
        print(url_params)
