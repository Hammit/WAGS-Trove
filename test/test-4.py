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
    'l-illustrated': 'true',
    'dateFrom': '1914-06-01',
    'dateTo': '1921-12-31',
    'encoding': TROVE_API_ENCODING
}

wa_newspapers = {
    'l-advtitle': 345,
    'l-advtitle': 344,
    'l-advtitle': 844,
    'l-advtitle': 933,
    'l-advtitle': 343,
    'l-advtitle': 275,
    'l-advtitle': 734,
    'l-advtitle': 934,
    'l-advtitle': 173,
    'l-advtitle': 221,
    'l-advtitle': 220,
    'l-advtitle': 811,
    'l-advtitle': 812,
    'l-advtitle': 813,
    'l-advtitle': 735,
    'l-advtitle': 814,
    'l-advtitle': 931,
    'l-advtitle': 180,
    'l-advtitle': 342,
    'l-advtitle': 928,
    'l-advtitle': 815,
    'l-advtitle': 816,
    'l-advtitle': 253,
    'l-advtitle': 817,
    'l-advtitle': 932,
    'l-advtitle': 846,
    'l-advtitle': 845,
    'l-advtitle': 736,
    'l-advtitle': 818,
    'l-advtitle': 254,
    'l-advtitle': 737,
    'l-advtitle': 738,
    'l-advtitle': 739,
    'l-advtitle': 819,
    'l-advtitle': 929,
    'l-advtitle': 255,
    'l-advtitle': 93,
    'l-advtitle': 740,
    'l-advtitle': 30,
    'l-advtitle': 98,
    'l-advtitle': 100,
    'l-advtitle': 101,
    'l-advtitle': 741,
    'l-advtitle': 820
}

wa_newspaper_ids = [
    345, 344, 844, 933, 343, 275, 734,
    934, 173, 221, 220, 811, 812, 813,
    735, 814, 931, 180, 342, 928, 815,
    816, 253, 817, 932, 846, 845, 736,
    818, 254, 737, 738, 739, 819, 929,
    255, 93,  740, 30,  98,  100, 101,
    741, 820
]
wa_newspaper_ids = { 'l-advtitle': wa_newspaper_ids }

request_params = params.copy()
request_params.update(wa_newspaper_ids)

r = requests.get(TROVE_API_URL_BASE, params=request_params)
print("Request URL: %s" % r.url)
if r.status_code == requests.codes.ok:
    print("Response: %s" % r.text)
    response = r.json()
    print("Response: Query == %s" % response['response']['query'])
    print("Response: Zone  == %s" % response['response']['zone'])

print("Finished")
