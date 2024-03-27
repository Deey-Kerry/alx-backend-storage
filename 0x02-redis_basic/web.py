#!/usr/bin/env python3
"""implement a get_page function (prototype: """
import requests
import time
from functools import lru_cache
url_access_count = {}


def cache_and_track(func):
    @lru_cache(maxsize=100)
    def wrapper(url):
        response = requests.get(url)
        page_content = response.text
        url_access_count[url] = url_access_count.get(url, 0) + 1
        time.sleep(10)
        return page_content
    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    return url


if __name__ == "__main__":
    url_ = "http://slowwly.robertomurray.co.uk/delay/1000/url/"
    url = f"{url_}http://www.google.com"
    print(get_page(url))
    print(get_page(url))
    print(f"Access count for {url}: {url_access_count[url]}")
