import asyncio
import struct 
import ssl
from urllib.parse import urlparse
from typing import Optional


class WebSocketClient:
    async def connect(self, url: str):
        parsed_url = urlparse(url)
        scheme, host, path = parsed_url.scheme, parsed_url.hostname, parsed_url.path or "/"
        port = parsed_url.port or (443 if scheme == "wss" else 80)
        ssl_context = ssl.create_default_context() if scheme == "wss" else None

        reader, writer = await asyncio.open_connection(host, port, ssl=ssl_context)
        key = "x3JJHMbDL1EzLkh9GBhXDw=="
        headers = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        writer.write(headers.encode())
        await writer.drain()

        response = await reader.read(1024)
        if b"101 Switching Protocols" not in response:
            raise Exception("Failed WebSocket handshake")

        return WebSocketConnection(reader, writer)


class WebSocketConnection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, message: str, is_ping: bool = False):
        """
        Send a message to the WebSocket.

        Args:
            message (str): The message to send.
            is_ping (bool): Whether this is a ping frame.
        """
        if is_ping:
            frame = b"\x89" + struct.pack("!B", len(message)) + message.encode()
        else:
            frame = b"\x81" + struct.pack("!B", len(message)) + message.encode()
        self.writer.write(frame)
        await self.writer.drain()



    async def receive(self) -> str:
        frame = await self.reader.read(1024)
        if not frame:
            raise ValueError("Empty frame received")
        opcode: int = frame[0] & 0x0F
        payload_length: int = frame[1] & 0x7F

        if opcode == 1:  # Text frame
            return frame[2:2 + payload_length].decode()
        elif opcode == 8:  # Close frame
            return "WebSocket closed"
        elif opcode in {9, 10}:  # Ping or Pong
            return "ping/pong"
        else:
            return f"Unsupported frame type: {opcode}"


    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
