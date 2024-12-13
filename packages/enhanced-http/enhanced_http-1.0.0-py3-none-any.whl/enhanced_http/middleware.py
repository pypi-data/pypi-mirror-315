from typing import Callable, Any, Dict, Union, List, Optional, Tuple, Awaitable
import asyncio


MiddlewareFunction = Callable[..., Union[Awaitable, Any]]


class MiddlewareManager:
    """
    A robust middleware manager that supports request/response middleware
    with optional prioritization and exception handling.

    ## Features
    - Prioritized execution of middleware.
    - Asynchronous and synchronous middleware support.
    - Exception-handling middleware.
    """

    def __init__(self):
        # Middleware chains
        self.request_middleware: List[Tuple[int, MiddlewareFunction]] = []
        self.response_middleware: List[Tuple[int, MiddlewareFunction]] = []

    def add_request_middleware(self, middleware: MiddlewareFunction, priority: int = 100) -> None:
        """
        Add a request middleware function.

        Args:
            middleware (MiddlewareFunction): The middleware function.
            priority (int): Middleware priority. Lower numbers run first.
        """
        self.request_middleware.append((priority, middleware))
        self.request_middleware.sort(key=lambda x: x[0])  # Sort by priority

    def add_response_middleware(self, middleware: MiddlewareFunction, priority: int = 100) -> None:
        """
        Add a response middleware function.

        Args:
            middleware (MiddlewareFunction): The middleware function.
            priority (int): Middleware priority. Lower numbers run first.
        """
        self.response_middleware.append((priority, middleware))
        self.response_middleware.sort(key=lambda x: x[0])  # Sort by priority

    async def apply_request(
        self, method: str, url: str, headers: Optional[Dict[str, str]], body: Optional[Any]
    ) -> Tuple[str, str, Dict[str, str], Any]:
        """
        Apply the request middleware chain.

        Args:
            method (str): HTTP method (e.g., GET, POST).
            url (str): Target URL.
            headers (Dict[str, str]): Request headers.
            body (Any): Request body.

        Returns:
            Tuple[str, str, Dict[str, str], Any]: Modified method, URL, headers, and body.
        """
        for _, middleware in self.request_middleware:
            if asyncio.iscoroutinefunction(middleware):
                method, url, headers, body = await middleware(method, url, headers, body)
            else:
                method, url, headers, body = middleware(method, url, headers, body)
        return method, url, headers or {}, body

    async def apply_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the response middleware chain.

        Args:
            response (Dict[str, Any]): The HTTP response object.

        Returns:
            Dict[str, Any]: The modified response object.
        """
        for _, middleware in self.response_middleware:
            if asyncio.iscoroutinefunction(middleware):
                response = await middleware(response)
            else:
                response = middleware(response)
        return response


# Prebuilt Middleware

async def logging_middleware_request(
    method: str, url: str, headers: Optional[Dict[str, str]], body: Optional[Any]
) -> Tuple[str, str, Dict[str, str], Any]:
    """
    Log HTTP request details.

    Args:
        method (str): HTTP method (e.g., GET, POST).
        url (str): Target URL.
        headers (Dict[str, str]): Request headers.
        body (Any): Request body.

    Returns:
        Tuple[str, str, Dict[str, str], Any]: Unmodified request details.
    """
    print(f"[Request] {method} {url} | Headers: {headers} | Body: {body}")
    return method, url, headers, body


async def logging_middleware_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Log HTTP response details.

    Args:
        response (Dict[str, Any]): The HTTP response object.

    Returns:
        Dict[str, Any]: The unmodified response object.
    """
    print(f"[Response] {response['status_code']} | Headers: {response['headers']} | Body: {response['body']}")
    return response


async def exception_handling_middleware_request(
    method: str, url: str, headers: Optional[Dict[str, str]], body: Optional[Any]
) -> Tuple[str, str, Dict[str, str], Any]:
    """
    Middleware for handling exceptions during request preprocessing.

    Args:
        method (str): HTTP method.
        url (str): Target URL.
        headers (Dict[str, str]): Request headers.
        body (Any): Request body.

    Returns:
        Tuple[str, str, Dict[str, str], Any]: Modified or unmodified request.
    """
    try:
        # Example: Simulate a validation step
        if not url.startswith("http"):
            raise ValueError(f"Invalid URL: {url}")
        return method, url, headers, body
    except Exception as e:
        print(f"[Middleware Exception] {e}")
        raise


async def add_default_headers_middleware(
    method: str, url: str, headers: Optional[Dict[str, str]], body: Optional[Any]
) -> Tuple[str, str, Dict[str, str], Any]:
    """
    Add default headers to all requests.

    Args:
        method (str): HTTP method.
        url (str): Target URL.
        headers (Dict[str, str]): Request headers.
        body (Any): Request body.

    Returns:
        Tuple[str, str, Dict[str, str], Any]: Modified request details.
    """
    headers = headers or {}
    headers.setdefault("User-Agent", "EnhancedHttpClient/1.0")
    headers.setdefault("Accept", "application/json")
    return method, url, headers, body
