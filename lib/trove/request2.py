import requests
import os
import shutil
from urllib.parse import urlparse


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
        return next_page_url is not None

    def next_page_url(self):
        try:
            next_page_url = self.json['response']['zone'][0]['records']['next']
        except KeyError:
            next_page_url = None

        return next_page_url


class TroveDownloader:
    def __init__(self, download_dir=None):
        if download_dir is not None:
            self.download_dir = download_dir
        else:
            self.download_dir = '/tmp/WAGS-Trove'

    def _image_path(self, url):
        parsed_url = urlparse(url)
        sections = parsed_url.path.split('/')
        image_name = sections[-1]
        path = os.path.join(self.download_dir, image_name)
        return path

    def download_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != requests.codes.ok:
            raise RuntimeError("{0} Error downloading image: {1}".format(r.status_code, url))
        else:
            path = self._image_path(url)
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
