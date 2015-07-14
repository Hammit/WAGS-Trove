#!/usr/bin/env python3

import os
import requests

TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')
TROVE_API_ENCODING = 'json'
TROVE_API_URL_BASE = 'http://api.trove.nla.gov.au/result'

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

r = requests.get(TROVE_API_URL_BASE, params=params)
if r.status_code == requests.codes.ok:
    response = r.json()
    print("Response: Query == %s" % response['response']['query'])
    print("Response: Zone  == %s" % response['response']['zone'])

print("Finished")
