#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from trove.request2 import *


TROVE_URL_BASE = 'http://trove.nla.gov.au'

# Config settings
config = ConfigParser()
config.read('../conf/config.ini')

image_path = config['DEFAULT']['image_download_path']
trove_api_key = config['DEFAULT']['trove_api_key']
trove_query = config['DEFAULT']['trove_query'] or ''
trove_zone = config['DEFAULT']['trove_zone'] or 'newspaper'

# Create the download dir if necessary
if Path(image_path).exists():
    print("Image download dir already exists")
else:
    print("Making download directory %s" % image_path)
    Path(image_path).mkdir(parents=True)

request = TroveRequest(trove_api_key)
request_params = {
    's': 0,
    'n': 75,
    'l-illustrated': 'Y',
    'l-availability': 'y/f',
    'reclevel': 'full',
}

response = request.query(trove_query, zone=trove_zone, params=request_params)
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
        if 'url' in article:
            print("\tURL: %s" % article['url'])

        if 'pdf' in article:
            print("\tPDF: %s" % article['pdf'])

        print("\tImage: %s" % image_url)

        r = requests.get(image_url)
        if r.status_code == requests.codes.ok:
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            image = soup.select('img#articleImg')[0]
            image_downloader = TroveDownloader(image_path)
            image_downloader.download_url(TROVE_URL_BASE + image['src'])

    # Get the next page if any
    if not response.has_next_page():
        break
    else:
        print("Getting the next page...")
        response = request.get_next_page(response)
