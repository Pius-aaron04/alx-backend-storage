#!/usr/bin/env python3

"""
This is an exercise file for redis basics
"""
import redis
from typing import Union, Callable, Optional
import uuid
import functools


class Cache:
    """
    A cache that stores data in redis
    """

    def count_calls(method: Callable) -> Callable:
        """
        function decorator to increment method calls
        """

        @functools.wraps(method)
        def increment(self, *args):
            """
            increaments calls
            """
            self._redis.incr(method.__qualname__)

            return method(self, *args)
        return increment

    def __init__(self) -> None:
        """
        instantiate redis
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[bytes, int, str, float]) -> str:
        """
        store data in redis with a random unique key
        """

        _id = str(uuid.uuid4())
        self._redis.set(_id, data)

        return _id

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[bytes, int, str, float]:
        """
        gets data from redis in desired format
        as provided by fn
        """

        data = self._redis.get(key)

        if fn is None:
            return data
        return fn(data)

    def get_str(self, data):
        """
        gets string format of data
        """

        return Cache.get(data, str)

    def get_int(self, data):
        """
        gets integer format of data
        """

        return Cache.get_str(data, int)
