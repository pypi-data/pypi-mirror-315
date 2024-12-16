import base64
from pathlib import Path
from typing import List, Dict, Any, Optional

from kiss_ai_stack_types.models import (
    DocumentsRequestBody,
    GenericResponseBody,
    QueryRequestBody,
    SessionRequest,
    SessionResponse,
    FileObject
)

from kiss_ai_stack_client.clients.rest_client import RestClient
from kiss_ai_stack_client.events.event_abc import EventAbc
from kiss_ai_stack_client.utils.logger import LOG


class RestEvent(EventAbc):
    def __init__(self, hostname: str, secure_protocol=True):
        """
        Initialize the RestEvent with a REST client.

        :param hostname: REST server hostname without protocol
        :param secure_protocol: Whether to use https or not.
        """
        self.__hostname = hostname
        self.__secure_protocol = secure_protocol
        self.__client: Optional[RestClient] = RestClient(
            base_url=f'{'https' if self.__secure_protocol else 'http'}://{hostname}')
        self.__session: Optional[SessionResponse] = None
        self.__headers: Dict[str, str] = {}

    def session(self) -> Optional[SessionResponse]:
        """
        Get the current session.

        :return: Current session response or None
        """
        return self.__session

    async def authorize_agent(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                              scope: Optional[str] = None) -> SessionResponse:
        """
        Authorize and create/refresh a session. Either a scope or client_id and client_secret is required.

        :param client_id: Generated client id from a previous auth session
        :param client_secret: Generated client secret from a previous auth session
        :param scope: 'temporary' or 'persistent'; temporary sessions may clean all the document data upon session closing.
        :return: Session response
        :raises Exception: If authorization fails
        """
        try:
            response = (await self.__client.post(
                url='/auth',
                headers={},
                params={},
                request_body=SessionRequest(
                    client_id=client_id,
                    client_secret=client_secret,
                    scope=scope
                ).model_dump(),
            )).json()
            if 'access_token' not in response:
                raise ValueError('No access token received')

            self.__session = SessionResponse(**response)
            self.__headers['Authorization'] = f"Bearer {self.__session.access_token}"

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
            if not self.__headers.get('Authorization'):
                LOG.warning('No active session to destroy')
                return GenericResponseBody(result='No active session')

            response = (await self.__client.post(
                url='/sessions',
                headers=self.__headers,
                params={'action': 'close'},
                request_body=QueryRequestBody(query=data if data else 'Goodbye!').model_dump()
            )).json()

            self.__session = None
            self.__headers.pop('Authorization', None)

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
            if not self.__headers.get('Authorization'):
                raise ValueError('No active session. Call authorize_agent first.')

            response = (await self.__client.post(
                url='/sessions',
                headers=self.__headers,
                params={'action': 'init'},
                request_body=QueryRequestBody(query=data).model_dump()
            )).json()

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
            if not self.__headers.get('Authorization'):
                raise ValueError('No active authorization. Call authorize_agent first.')

            response = (await self.__client.post(
                url='/queries',
                headers=self.__headers,
                params={},
                request_body=QueryRequestBody(query=data).model_dump()
            )).json()

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
            if not self.__headers.get('Authorization'):
                raise ValueError('No active authorization. Call authorize_agent first.')

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

            response = (await self.__client.post(
                url='/documents',
                headers=self.__headers,
                request_body=DocumentsRequestBody(
                    files=encoded_files,
                    metadata=metadata or {}
                ).model_dump()
            )).json()

            return GenericResponseBody(**response)

        except Exception as e:
            LOG.error(f'Failed to store documents: {str(e)}')
            raise
