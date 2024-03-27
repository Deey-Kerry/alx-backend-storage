#!/usr/bin/env python3
"""Redis Exercises combined"""
import sys
from typing import Union, Callable, Optional
from uuid import uuid4
import redis
from functools import wraps
UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """counting number of times cache class called"""
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    key = method.__qualname__
    input_i = "".join([key, ":inputs"])
    output = "".join([key, ":outputs"])
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method"""
        self._redis.rpush(input_i, str(args))
        out = method(self, *args, **kwargs)
        self._redis.rpush(output, str(out))
        return out
    return wrapper


class Cache:
    """Writing strings to Redis"""
    def __init__(self):
        """ store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """method should generate a random key (e.g. using uuid), store
        the input data in Redis using the random key and return the key"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """convert the data back to the desired format"""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_int(self: bytes) -> int:
        """parametrize Cache.get with the correct conversion function"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """parametrize Cache.get with the correct conversion function."""
        return self.decode("utf-8")
