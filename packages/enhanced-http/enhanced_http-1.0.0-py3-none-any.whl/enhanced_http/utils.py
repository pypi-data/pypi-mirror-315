import asyncio


async def async_retry(func, retries=3, backoff_factor=0.5, *args, **kwargs):
    """
    Retry a coroutine function with exponential backoff.

    :param func: Coroutine function to retry.
    :param retries: Number of retries.
    :param backoff_factor: Initial backoff factor (seconds).
    :param args: Positional arguments for the coroutine function.
    :param kwargs: Keyword arguments for the coroutine function.
    :return: The result of the coroutine function.
    """
    for attempt in range(retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt < retries:
                backoff_time = backoff_factor * (2 ** attempt)
                await asyncio.sleep(backoff_time)
            else:
                raise e
