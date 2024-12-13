import time
from typing import Optional, Dict, Any


class InMemoryCache:
    """
    A simple in-memory caching backend for storing key-value pairs with TTL (time-to-live).

    ## Features
    - Set and retrieve cached values
    - Automatic expiration of keys based on TTL
    """

    def __init__(self):
        """
        Initialize the in-memory cache.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Args:
            key (str): The key to look up in the cache.

        Returns:
            Optional[Any]: The cached value, or None if the key does not exist or has expired.
        """
        entry = self.cache.get(key)
        if entry and entry["expires_at"] > time.time():
            return entry["value"]
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """
        Set a value in the cache.

        Args:
            key (str): The key to store in the cache.
            value (Any): The value to cache.
            ttl (int): Time-to-live for the key in seconds. Defaults to 300 seconds.
        """
        self.cache[key] = {"value": value, "expires_at": time.time() + ttl}
