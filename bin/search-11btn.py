#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import shutil
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from trove.request import Request as TroveRequest
from trove.request import NewspaperTitlesRequest as TroveNewspaperTitlesRequest


def image_path(url):
    parsed_url = urlparse(url)
    sections = parsed_url.path.split('/')
    image_name = sections[-1]
    path = '/tmp/' + image_name
    return path


def download_image(url):
    r = requests.get(url, stream=True)
    if r.status_code != requests.codes.ok:
        raise RuntimeError("{0} Error downloading image: {1}".format(r.status_code, url))
    else:
        path = image_path(url)
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


TROVE_URL_BASE = 'http://trove.nla.gov.au'
TROVE_API_KEY = os.getenv('TROVE_API_KEY', '')

newspapers = TroveNewspaperTitlesRequest(TROVE_API_KEY)

trove = TroveRequest(TROVE_API_KEY)
query_params = {
    'l-illustrated': 'Y',                       # contains images
    'l-title': newspapers.get_ids(state='wa'),  # restrict to given newspapers
    'reclevel': 'full',                         # full detail records
    's': 0,                                     # start
    'n': 25,                                    # n results
}
trove.get(query='11th Battalion date:[1914 TO 1921]', params=query_params)

print("Request URL: %s" % trove.response.url)
if trove.response.status_code != requests.codes.ok:
    print("Error: Problem processing request")
else:
    # print("Response: %s" % trove.response.text)
    response = trove.response.json()
    # print("Response Records: %s" % response['response'])
    print("%s Records (Total)" % response['response']['zone'][0]['records']['total'])
    for article in response['response']['zone'][0]['records']['article']:
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
            download_image(TROVE_URL_BASE + image['src'])
