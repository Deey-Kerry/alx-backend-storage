#!/usr/bin/env python3
"""Cache class. In the __init__ method, store an instance of the
Redis client as a private variable named _redis (using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string. The method should generate a random key (e.g. using uuid), store the input data in Redis using the random key and return the key.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps
UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """Counts number of times of Cache class"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Function that wraps arguements
        """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Calls history in the methods which are callable"""
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """ Wrapper function for calls"""
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper


class Cache:
    """Class for the cache """
    def __init__(self):
        """ Initializes the function """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def (self,
              data: UnionOfTypes) -> str:
        """Function that has Union of Types"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> UnionOfTypes:
        """gets strings for the Union of Types"""
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """gets a string for the key"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ Gets integer"""
        return self.get(key, int)
