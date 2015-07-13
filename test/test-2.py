#!/usr/bin/env python3

import os
import urllib.parse
import requests

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
r = requests.get(url)
if r.status_code == requests.codes.ok:
    response_json = r.json()
    print("Response: Query == %s" % response_json['response']['query'])
    print("Response: Zone  == %s" % response_json['response']['zone'])

print("Finished")
