#!/usr/bin/env python3
"""web cache and wrapper"""
import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """Gets requests from url
    """
    r.set(f"cached:{url}", count)
    req = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return req.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
