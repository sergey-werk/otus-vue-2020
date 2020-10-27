#!/usr/bin/env python3
import time
import requests

i = 0
while True:
    try:
        requests.get('http://localhost:5000/api/items/0/update?title={}'.format(i))
        i += 1
        # print('.', flush=True, end='')
    except requests.exceptions.ConnectionError:
        pass
    time.sleep(0.01)