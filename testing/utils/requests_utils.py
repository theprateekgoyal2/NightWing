import requests
import json
import os
from testing.urls.popscape_urls import *

def hit_endpoint(endpoint, method, payload=None, params=None):
    url = f'{domain}{endpoint}'
    payload = json.dumps(payload)
    return requests.request(method=method.upper(), url=url, headers=headers, data=payload, params=params)