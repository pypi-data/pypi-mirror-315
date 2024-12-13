import pytest
from enhanced_http.cache import InMemoryCache
import asyncio


@pytest.mark.asyncio
async def test_cache_set_and_get():
    """
    Test setting and retrieving values from the cache.
    """
    cache = InMemoryCache()
    await cache.set("key1", "value1", ttl=10)
    value = await cache.get("key1")

    assert value == "value1", "Cache retrieval failed for 'key1'."


@pytest.mark.asyncio
async def test_cache_expiration():
    """
    Test cache expiration behavior after TTL.
    """
    cache = InMemoryCache()
    await cache.set("key2", "value2", ttl=2)
    await asyncio.sleep(3)  # Wait for TTL to expire

    value = await cache.get("key2")
    assert value is None, "Cache did not expire as expected."


@pytest.mark.asyncio
async def test_cache_overwrite():
    """
    Test overwriting an existing cache key.
    """
    cache = InMemoryCache()
    await cache.set("key3", "value3", ttl=10)
    await cache.set("key3", "new_value3", ttl=10)
    value = await cache.get("key3")

    assert value == "new_value3", "Cache overwrite failed for 'key3'."


@pytest.mark.asyncio
async def test_large_ttl():
    """
    Test setting a cache key with a large TTL value.
    """
    cache = InMemoryCache()
    await cache.set("key4", "value4", ttl=3600)  # 1 hour TTL
    value = await cache.get("key4")

    assert value == "value4", "Cache failed with a large TTL."


@pytest.mark.asyncio
async def test_cache_no_ttl():
    """
    Test default TTL behavior when none is provided.
    """
    cache = InMemoryCache()
    await cache.set("key5", "value5")
    value = await cache.get("key5")

    assert value == "value5", "Cache failed to store a value without a specified TTL."


@pytest.mark.asyncio
async def test_get_nonexistent_key():
    """
    Test retrieving a nonexistent cache key.
    """
    cache = InMemoryCache()
    value = await cache.get("nonexistent_key")

    assert value is None, "Nonexistent key should return None."
