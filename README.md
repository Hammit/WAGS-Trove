# WAGS-Trove

## Dependencies

* Python 3.4
* Requests
* Beautiful Soup 4

Install these dependencies on an Ubuntu system with

`sudo apt-get install python3 python3-requests python3-bs4`

## NOTES

You can get away with using a Python version less than 3.4, like 3.3, but you need to install pathlib.

`sudo apt-get install python3-pip`
`sudo pip install pathlib`

To run '/bin/download-images.py' you need '/conf/config.ini' setup correctly

`
[DEFAULT]
image_download_path = /tmp/WAGS-Trove
trove_api_key = <INSERT API KEY HERE>
trove_query = "11th Battalion" date:[1914 TO 1921]
trove_zone = newspaper
`

## TODO

Use a config file for things like temp directory to use and api key, etc
Auto create temp dir if needed
Search trove for illustrated articles only (l-illustrated)
