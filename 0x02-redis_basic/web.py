#!/usr/bin/env python3
"""web task"""
import requests
import time
from functools import wraps

CACHE = {}

def cache_with_expiry(expiration_time):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            current_time = time.time()
            if url in CACHE and current_time - CACHE[url]["timestamp"] < expiration_time:
                CACHE[url]["count"] += 1
                print(f"Cache hit for {url}, accessed {CACHE[url]['count']} times.")
                return CACHE[url]["content"]
            else:
                content = func(url)
                CACHE[url] = {"content": content, "timestamp": current_time, "count": 1}
                print(f"Cache miss for {url}.")
                return content
        return wrapper
    return decorator

@cache_with_expiry(10)
def get_page(url):
    response = requests.get(url)
    return response.text

# Testing the function
if __name__ == "__main__":
    # Testing with a slow response URL
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(slow_url))  # This should take some time due to the slow response
    print(get_page(slow_url))  # This should be faster due to caching
    
    # Testing with a regular URL
    regular_url = "http://www.example.com"
    print(get_page(regular_url))  # This should be fetched and displayed
    print(get_page(regular_url))  # This should be faster due to caching
