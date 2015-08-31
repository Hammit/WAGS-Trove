#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read('../conf/config.ini')

image_path = config['DEFAULT']['image_download_path']
print("Image Path: %s" % image_path)

if Path(image_path).exists():
    print("Image path already exists")
else:
    print("Making directory %s" % image_path)
    Path(image_path).mkdir(parents=True)

api_key = config['DEFAULT']['trove_api_key']
print("API Key: %s" % api_key)

query = config['DEFAULT']['trove_query']
print("Query: '%s'" % query)

# non_existant = config['DEFAULT']['blahblah']
# print("Non Existant Key: %s" % non_existant)
