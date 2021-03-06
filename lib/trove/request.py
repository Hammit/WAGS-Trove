import requests
import os
import shutil
from urllib.parse import urlparse


class Request:
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


class NewspaperTitlesRequest:
    API_URL_BASE = 'http://api.trove.nla.gov.au/newspaper/titles'
    API_ENCODING = 'json'

    def __init__(self, api_key=''):
        self.params = {
            'key': api_key,
            'encoding': self.API_ENCODING
        }
        self.response = None       # response object from requests.get
        self.response_json = None  # python dict from calling .json()

    def get_ids(self, state='wa'):
        params = {
            'state': state
        }
        params.update(self.params)
        self.response = requests.get(self.API_URL_BASE, params=params)
        self.response_json = self.response.json()

        ids = []
        newspapers = self.response_json['response']['records']['newspaper']
        for newspaper in newspapers:
            ids.append(newspaper['id'])
        return ids

    def url_params(self, newspaper_ids=[]):
        url_params = ""
        for newspaper_id in newspaper_ids:
            url_params += "l-title={0}&".format(newspaper_id)
        url_params.rstrip('&')
        return url_params

    def get_str(self, state='wa'):
        params = {
            'state': state
        }
        params.update(self.params)

        self.response = requests.get(self.API_URL_BASE, params=params)
        if self.response.status_code != requests.codes.ok:
            return None
        else:
            # print("Response: %s" % r.text)
            self.response_json = self.response.json()
            newspaper_ids = self.get_ids()
            # print("Newspaper Ids: %s" % newspaper_ids)
            # print("Response Records: %s" % response['response']['records']['newspaper'])
            url_params = self.url_params(newspaper_ids)
            return url_params


class Downloader:
    BASE_DIR = '/tmp/WAGS-Trove'

    @classmethod
    def _image_path(cls, url):
        parsed_url = urlparse(url)
        sections = parsed_url.path.split('/')
        image_name = sections[-1]
        path = os.path.join(cls.BASE_DIR, image_name)
        return path

    @classmethod
    def download_url(cls, url):
        r = requests.get(url, stream=True)
        if r.status_code != requests.codes.ok:
            raise RuntimeError("{0} Error downloading image: {1}".format(r.status_code, url))
        else:
            path = cls._image_path(url)
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
