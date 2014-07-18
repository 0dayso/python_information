__author__ = 'Han'

import requests
import json

api_key = 'AIzaSyBba8-GM8S-7ADUKfHfu0k91q0MBJWuOMk'

def google_decode(address):
    #reformat address
    address_fmt = address
    variable = {'address':address_fmt, 'key': api_key}
    results = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params = variable)
    results_json = json.loads(results.text)
    return results_json