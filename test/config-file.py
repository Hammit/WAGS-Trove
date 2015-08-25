#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read('../conf/config.ini')

image_path = config['DEFAULT']['image_download_path']
print("Image Path: %s" % image_path)

api_key = config['DEFAULT']['trove_api_key']
print("API Key: %s" % api_key)


if Path(image_path).exists():
    print("Image path already exists")
else:
    print("Making directory %s" % image_path)
    Path(image_path).mkdir(parents=True)
