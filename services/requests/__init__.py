from time import sleep

import requests


def get_page(url, params):
    for attempt in range(10):
        try:
            response = requests.get(url, params)
            if response.ok:
                return response.text
        except requests.RequestException as e:
            print(f"Request error on {url}: {e}")
        sleep(1)
    raise ValueError(f"Failed to fetch data after 10 attempts")
