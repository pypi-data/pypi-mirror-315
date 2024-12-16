import base64
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from kiss_ai_stack_types.enums import ServerEvent
from kiss_ai_stack_types.models import GenericResponseBody, FileObject, SessionResponse, SessionRequest

from kiss_ai_stack_client.clients.rest_client import RestClient
from kiss_ai_stack_client.clients.ws_client import WebSocketClient
from kiss_ai_stack_client.events.event_abc import EventAbc
from kiss_ai_stack_client.utils.logger import LOG


class WebSocketEvent(EventAbc):
    def __init__(self, hostname: str, secure_protocol: bool = True):
        """
        Initialize the WebSocketEvent with a WebSocket client.

        :param hostname: WebSocket client's hostname without protocol
        :param secure_protocol: Whether to use secure transport or not
        """
        self.__hostname = hostname
        self.__secure_protocol = secure_protocol
        self.__headers: Optional[Dict[str, str]] = None
        self.__client: Optional[WebSocketClient] = None
        self.__session: Optional[SessionResponse] = None

    async def __send_message(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a message to the WebSocket server and receive a response.

        :param event: Event type to send
        :param data: Data to send with the event
        :return: The server's response
        """
        if not self.__client or not self.__client.websocket:
            await self.init_client()
        message = {'event': event, 'data': data if data else ''}
        LOG.info(f'Sending message: {message}')
        await self.__client.websocket.send(json.dumps(message))
        response = await self.__client.websocket.recv()
        LOG.info(f'Received response: {response}')
        return json.loads(response)

    async def init_client(self):
        self.__client = WebSocketClient(
            f'{'wss' if self.__secure_protocol else 'ws'}://{self.__hostname}/ws',
            extra_headers=self.__headers
        )
        await self.__client.connect()

    async def authorize_agent(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                              scope: Optional[str] = None) -> SessionResponse:
        """
        AAuthorize and create/refresh a session. Either a scope or client_id and client_secret is required.

        :param client_id: Generated client id from a previous auth session
        :param client_secret: Generated client secret from a previous auth session
        :param scope: 'temporary' or 'persistent'; temporary sessions may clean all the document data upon session closing.
        :return: Session response
        """
        try:
            http_client = RestClient(f'{'https' if self.__secure_protocol else 'http'}://{self.__hostname}')
            session_result = (await http_client.post(
                url='/auth',
                headers={},
                params={},
                request_body=SessionRequest(
                    client_id=client_id,
                    client_secret=client_secret,
                    scope=scope
                ).model_dump(),
            )).json()
            if 'access_token' not in session_result:
                raise ValueError('No access token received')

            self.__session = SessionResponse(**session_result)
            self.__headers = {'Authorization': f"Bearer {self.__session.access_token}"}

            if not self.__client:
                await self.init_client()
            return self.__session

        except Exception as e:
            LOG.error(f'Authorization failed: {str(e)}')
            raise

    async def destroy_agent(self, data: Optional[str] = None) -> GenericResponseBody:
        """
        Destroy/close the current agent session.

        :param data: Optional query
        :return: Generic response body with session closure result
        """
        try:
            response = await self.__send_message(ServerEvent.ON_CLOSE, {'query': data if data else 'Goodbye!'})
            await self.__client.close()
            return GenericResponseBody(**response)

        except Exception as e:
            LOG.error(f'Failed to destroy agent session: {str(e)}')
            raise

    async def bootstrap_agent(self, data: Optional[str] = None) -> GenericResponseBody:
        """
        Initialize and start the AI agent.

        :param data: Optional query
        :return: Generic response body with bootstrap result
        """
        try:
            response = await self.__send_message(ServerEvent.ON_INIT, {'query': data if data else 'Greetings!'})
            return GenericResponseBody(**response)

        except Exception as e:
            LOG.error(f'Failed to bootstrap agent: {str(e)}')
            raise

    async def generate_answer(self, data: Optional[str]) -> GenericResponseBody:
        """
        Generate an answer based on the query.

        :param data: Query request body
        :return: Generic response body with generated answer
        """
        try:
            response = await self.__send_message(ServerEvent.ON_QUERY, {'query': data})
            return GenericResponseBody(**response)

        except Exception as e:
            LOG.error(f'Failed to generate answer: {str(e)}')
            raise

    async def store_data(self, files: List[str], metadata: Optional[Dict[str, Any]] = None) -> GenericResponseBody:
        """
        Store documents with optional metadata.

        :param files: List of file paths to store
        :param metadata: Optional metadata for the files
        :return: Generic response body with storage result
        """
        try:
            encoded_files: List[FileObject] = []
            for file_path in files:
                file_path = Path(file_path)

                if not file_path.exists():
                    LOG.warning(f'File not found: {file_path}')
                    continue

                with open(file_path, 'rb') as file:
                    encoded_content = base64.b64encode(file.read()).decode('utf-8')
                    encoded_files.append(FileObject(
                        name=file_path.name,
                        content=encoded_content
                    ))

            if not encoded_files:
                raise ValueError('No valid files to store')

            response = await self.__send_message(ServerEvent.ON_STORE, {
                'files': [f.dict() for f in encoded_files],
                'metadata': metadata or {}
            })
            return GenericResponseBody(**response)

        except Exception as e:
            LOG.error(f'Failed to store documents: {str(e)}')
            raise
