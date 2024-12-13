import pytest
from enhanced_http.websocket import WebSocketClient


@pytest.mark.asyncio
async def test_websocket_connect():
    """
    Test establishing a WebSocket connection.
    """
    ws_client = WebSocketClient()
    ws_conn = await ws_client.connect("wss://echo.websocket.org")
    assert ws_conn is not None, "WebSocket connection failed."
    await ws_conn.close()


@pytest.mark.asyncio
async def test_websocket_send_and_receive():
    ws_client = WebSocketClient()
    ws_conn = await ws_client.connect("wss://ws.postman-echo.com/raw")

    message = "Hello, WebSocket!"
    await ws_conn.send(message)
    response = await ws_conn.receive()

    assert response == message, f"Expected '{message}', got '{response}'."
    print(response)
    await ws_conn.close()


@pytest.mark.asyncio
async def test_websocket_close():
    """
    Test closing a WebSocket connection and ensure further operations fail.
    """
    ws_client = WebSocketClient()
    ws_conn = await ws_client.connect("wss://echo.websocket.org")
    await ws_conn.close()

    with pytest.raises(ConnectionResetError):
        await ws_conn.send("This should fail.")


@pytest.mark.asyncio
async def test_websocket_ping_pong():
    ws_client = WebSocketClient()
    ws_conn = await ws_client.connect("wss://ws.postman-echo.com/raw")

    # Send a ping frame manually and receive a pong response
    await ws_conn.send("ping", is_ping=True)
    response = await ws_conn.receive()

    assert response == "ping/pong", "WebSocket ping/pong failed."
    await ws_conn.close()
