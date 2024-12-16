from typing import Dict, Optional, Any

import websockets
from websockets.exceptions import (
    WebSocketException,
    ConnectionClosed,
    InvalidStatus
)

from kiss_ai_stack_client.utils.logger import LOG


class WebSocketClient:
    def __init__(
            self,
            url: str,
            extra_headers: Optional[Dict[str, str]] = None,
            ping_interval: Optional[float] = 20,
            ping_timeout: Optional[float] = 20
    ):
        """
        Initialize WebSocket client.

        :param url: WebSocket server URL
        :param extra_headers: Optional headers to send with connection
        :param ping_interval: Interval between ping messages (in seconds)
        :param ping_timeout: Timeout for ping responses (in seconds)
        """
        self.url = url
        self.extra_headers = extra_headers or {}
        self.websocket = None
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout

    async def connect(self):
        """
        Establish WebSocket connection with robust error handling.

        :return: WebSocket connection
        :raises WebSocketException: If connection fails
        """
        try:
            if not isinstance(self.extra_headers, dict):
                raise ValueError('Headers must be a dictionary')
            LOG.info(f'Connecting to {self.url}')
            self.websocket = await websockets.connect(
                self.url,
                additional_headers=self.extra_headers
            )
            LOG.info('WebSocket connection established')
            return self.websocket

        except InvalidStatus as e:
            LOG.error(f'Invalid HTTP status code: {e}')
            raise
        except ConnectionRefusedError as e:
            LOG.error(f'Connection refused: {e}')
            raise
        except WebSocketException as e:
            LOG.error(f'WebSocket connection error: {e}')
            raise
        except Exception as e:
            LOG.error(f'Unexpected connection error: {e}')
            raise

    async def close(self) -> None:
        """
        Safely close the WebSocket connection.
        """
        if self.websocket:
            try:
                await self.websocket.close()
                LOG.info('WebSocket connection closed')
            except Exception as e:
                LOG.warning(f'Error closing WebSocket: {e}')
            finally:
                self.websocket = None

    async def send(self, message: Any) -> None:
        """
        Send a message through the WebSocket.

        :param message: Message to send
        :raises ConnectionClosed: If connection is closed
        """
        if not self.websocket:
            raise ConnectionClosed(None, None)

        try:
            await self.websocket.send(message)
            LOG.debug(f'Message sent: ****')
        except ConnectionClosed:
            LOG.error('Cannot send message: WebSocket connection closed')
            raise

    async def receive(self) -> str:
        """
        Receive a message from the WebSocket.

        :return: Received message
        :raises ConnectionClosed: If connection is closed
        """
        if not self.websocket:
            raise ConnectionClosed(None, None)

        try:
            message = await self.websocket.recv()
            LOG.debug('Message received: ****')
            return message
        except ConnectionClosed:
            LOG.error('Cannot receive message: WebSocket connection closed')
            raise
