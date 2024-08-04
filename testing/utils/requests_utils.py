import requests
import json
import os
from testing.urls.popscape_urls import *

def hit_endpoint(endpoint, payload, method, params=None):
    print(params)
    # domain=popscape_urls.domain
    # headers=popscape_urls.headers
    url = f'{domain}{endpoint}'
    print(f"url == {url}")
    payload = json.dumps(payload)
    return requests.request(method=method.upper(), url=url, headers=headers, data=payload, params=params)