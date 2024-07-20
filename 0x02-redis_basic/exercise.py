#!/usr/bin/env python3

"""
This is an exercise file for redis basics
"""

import redis
from typing import Union, Callable
import uuid


class Cache:
    """
    A cache that stores data in redis
    """

    def __init__(self) -> None:
        """
        instantiate redis
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[bytes, int, str, float]) -> str:
        """
        store data in redis with a random unique key
        """

        _id = str(uuid.uuid4())
        self._redis.set(_id, data)

        return _id

    def get(self, key: str, fn: Callable):
        """
        gets data from redis in desired format
        as provided by fn
        """

        data = self._redis.get(key)

        return fn(data)

    def get_str(self, data):
        """
        gets string format of data
        """

        return str(data)

    def get_int(self, data):
        """
        gets integer format of data
        """

        return int(data)
