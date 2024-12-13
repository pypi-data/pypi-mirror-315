import asyncio
import ssl
import json
from typing import Optional, Union, Dict, Tuple, Any
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.DEBUG)

class EnhancedHttpClient:
    def __init__(
        self,
        max_retries: int = 2,
        backoff_factor: float = 0.5,
        sock_connect_timeout: float = 10.0,
        sock_read_timeout: float = 10.0,
        max_concurrent_requests: int = 5,
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.sock_connect_timeout = sock_connect_timeout
        self.sock_read_timeout = sock_read_timeout
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, Dict, bytes]] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], Tuple[asyncio.StreamReader, asyncio.StreamWriter]]:
        async with self.semaphore:
            parsed_url = urlparse(url)
            scheme, host, path = parsed_url.scheme, parsed_url.hostname, parsed_url.path or "/"
            port = parsed_url.port or (443 if scheme == "https" else 80)
            ssl_context = ssl.create_default_context() if scheme == "https" else None

            # Prepare body and headers
            data, headers = self._prepare_body(body, headers)
            headers["Host"] = host

            for attempt in range(self.max_retries + 1):
                writer = None
                try:
                    logging.debug(f"Attempting connection to {host}:{port} (Attempt {attempt + 1})")
                    reader, writer = await asyncio.open_connection(host, port, ssl=ssl_context)
                    request_line = f"{method} {path} HTTP/1.1\r\n"
                    headers_section = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
                    writer.write((request_line + headers_section + "\r\n").encode("utf-8"))
                    if data:
                        writer.write(data)
                    await writer.drain()

                    if stream:
                        return reader, writer  # Return the raw reader and writer for streaming

                    # Read the response with timeouts
                    status_line = await asyncio.wait_for(reader.readline(), timeout=self.sock_read_timeout)
                    status_line = status_line.decode('utf-8').strip()
                    status_code = int(status_line.split(' ')[1])

                    # Read headers with timeouts
                    headers_response = {}
                    while True:
                        line = await asyncio.wait_for(reader.readline(), timeout=self.sock_read_timeout)
                        if line in (b'\r\n', b'\n', b''):
                            break
                        key_value = line.decode('utf-8').strip()
                        if ': ' in key_value:
                            key, value = key_value.split(': ', 1)
                            headers_response[key.strip()] = value.strip()

                    # Read body with timeouts
                    if 'Content-Length' in headers_response:
                        content_length = int(headers_response['Content-Length'])
                        body = await asyncio.wait_for(reader.readexactly(content_length), timeout=self.sock_read_timeout)
                    elif headers_response.get('Transfer-Encoding', '').lower() == 'chunked':
                        body = await asyncio.wait_for(self._read_chunked_body(reader), timeout=self.sock_read_timeout)
                    else:
                        # Read until EOF
                        body = await asyncio.wait_for(reader.read(), timeout=self.sock_read_timeout)

                    # Close the connection
                    writer.close()
                    await writer.wait_closed()

                    # Parse body as JSON if possible
                    try:
                        body_decoded = body.decode('utf-8')
                        body_json = json.loads(body_decoded)
                        body = body_json
                    except json.JSONDecodeError:
                        body = body.decode('utf-8')

                    return {"status_code": status_code, "headers": headers_response, "body": body}

                except asyncio.TimeoutError as e:
                    logging.warning(f"Timeout on attempt {attempt + 1}: {e}")
                    if attempt >= self.max_retries:
                        raise asyncio.TimeoutError("Request timed out after retries") from e
                    await asyncio.sleep(self.backoff_factor * (2 ** attempt))
                except ssl.SSLError as e:
                    logging.error(f"SSL error on attempt {attempt + 1}: {e}")
                    if attempt >= self.max_retries:
                        raise
                    await asyncio.sleep(self.backoff_factor * (2 ** attempt))
                finally:
                    if writer and not stream:
                        try:
                            writer.close()
                            await writer.wait_closed()
                        except ssl.SSLError as e:
                            if "APPLICATION_DATA_AFTER_CLOSE_NOTIFY" not in str(e):
                                raise

    def _prepare_body(
        self, body: Optional[Union[str, Dict, bytes]], headers: Optional[Dict]
    ) -> Tuple[Optional[bytes], Dict]:
        headers = headers.copy() if headers else {}

        if body is None:
            return None, headers

        if isinstance(body, dict):
            body = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(body, str):
            headers.setdefault("Content-Type", "application/json")
            body = body.encode("utf-8")
        elif isinstance(body, bytes):
            headers.setdefault("Content-Type", "application/octet-stream")
        else:
            raise ValueError(f"Unsupported body type: {type(body)}. Must be str, dict, or bytes.")

        headers["Content-Length"] = str(len(body))
        return body, headers

    async def _read_chunked_body(self, reader):
        body = b''
        while True:
            # Read the chunk size line with timeout
            line = await asyncio.wait_for(reader.readline(), timeout=self.sock_read_timeout)
            chunk_size_str = line.strip()
            if b';' in chunk_size_str:
                chunk_size_str = chunk_size_str.split(b';', 1)[0]
            if not chunk_size_str:
                break
            chunk_size = int(chunk_size_str, 16)
            if chunk_size == 0:
                # Last chunk
                break
            # Read the chunk data with timeout
            chunk_data = await asyncio.wait_for(reader.readexactly(chunk_size), timeout=self.sock_read_timeout)
            body += chunk_data
            # Read the trailing \r\n after chunk with timeout
            await asyncio.wait_for(reader.readline(), timeout=self.sock_read_timeout)
        # Read any trailing headers after the last chunk with timeout
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=self.sock_read_timeout)
            if line in (b'\r\n', b'\n', b''):
                break
        return body
