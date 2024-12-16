from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from kiss_ai_stack_types.models import GenericResponseBody, SessionResponse


class EventAbc(ABC):
    @abstractmethod
    async def authorize_agent(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                              scope: Optional[str] = None) -> SessionResponse:
        pass

    @abstractmethod
    async def destroy_agent(self, data: Optional[str] = None) -> GenericResponseBody:
        pass

    @abstractmethod
    async def bootstrap_agent(self, data: Optional[str] = None) -> GenericResponseBody:
        pass

    @abstractmethod
    async def generate_answer(self, data: Optional[str]) -> GenericResponseBody:
        pass

    @abstractmethod
    async def store_data(self, files: List[str], metadata: Optional[Dict[str, Any]] = None) -> GenericResponseBody:
        pass
