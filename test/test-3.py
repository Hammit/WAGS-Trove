#!/usr/bin/env python3

import os
import urllib.request
import urllib.parse
import json

TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')
TROVE_API_ENCODING = 'json'
TROVE_API_URL_BASE = 'http://api.trove.nla.gov.au/result?%s'

zone  = 'newspaper'
query = '11th Battalion'
params = {
    'key': TROVE_API_KEY,
    'zone': zone,
    'q': query,
    'n': 50,
    's': 0,
    'encoding': TROVE_API_ENCODING
}
url_params = urllib.parse.urlencode(params)
url = TROVE_API_URL_BASE % url_params
print("Request: %s" % url)
response = urllib.request.urlopen(url)
response_str = response.readall().decode('utf-8')
print(response_str)
response_data = json.loads(response_str)
print("Query: %s" % response_data['response']['query'])
print("Finished")
