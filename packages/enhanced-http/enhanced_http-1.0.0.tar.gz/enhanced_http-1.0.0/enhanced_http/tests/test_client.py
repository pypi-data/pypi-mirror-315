import pytest
import json
import asyncio
from enhanced_http.client import EnhancedHttpClient

@pytest.mark.asyncio
async def test_get_request():
    client = EnhancedHttpClient(sock_read_timeout=30)
    response = await client.request("GET", "https://httpbin.org/get")
    assert response["status_code"] == 200, f"Unexpected status code: {response['status_code']}"

@pytest.mark.asyncio
async def test_post_request():
    client = EnhancedHttpClient(sock_read_timeout=30)
    response = await client.request(
        "POST",
        "https://httpbin.org/post",
        headers={"Content-Type": "application/json"},
        body=json.dumps({"key": "value"}),
    )
    print(response)
    assert response["status_code"] == 200, f"Unexpected status code: {response['status_code']}"
    body_json = response["body"]
    assert body_json["json"] == {"key": "value"}, f"Response JSON mismatch: {body_json}"

@pytest.mark.asyncio
async def test_retries():
    client = EnhancedHttpClient(max_retries=3, backoff_factor=0.5, sock_read_timeout=2)
    with pytest.raises(asyncio.TimeoutError, match="Request timed out after retries"):
        await client.request("GET", "https://httpbin.org/delay/10")

@pytest.mark.asyncio
async def test_streaming_response():
    client = EnhancedHttpClient(sock_read_timeout=30)
    stream_reader, writer = await client.request("GET", "https://httpbin.org/stream/5", stream=True)
    assert stream_reader is not None

    lines = []
    try:
        while not stream_reader.at_eof():
            line = await stream_reader.readline()
            if line:
                lines.append(line.decode().strip())
    except Exception as e:
        pytest.fail(f"Streaming error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
    assert len(lines) > 0, "No lines were streamed"
