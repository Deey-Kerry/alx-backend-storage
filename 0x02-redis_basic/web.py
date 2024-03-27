#!/usr/bin/env python3
"""
Caching request module with tracking and expiration time
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()

def count_access_and_cache(expiration_time=10):
    """Decorator to count the number of accesses to a URL and cache the content."""
    def decorator(func):
        @wraps(func)
        def wrapper(url: str) -> str:
            # Increment the access count for the URL
            redis_client.incr(f"count:{url}")
            # Attempt to get the cached content
            cached_content = redis_client.get(url)
            if cached_content:
                return cached_content.decode('utf-8')
            else:
                # Fetch the page content as it's not cached
                response = func(url)
                # Cache the content with the specified expiration time
                redis_client.setex(url, expiration_time, response)
                return response
        return wrapper
    return decorator

@count_access_and_cache(expiration_time=10)
def get_page(url: str) -> str:
    """Makes a HTTP request to a given endpoint."""
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
