import requests
import aiohttp
from typing import Dict, Any
from pydantic import BaseModel

class ModusClient(BaseModel):
    """Authenticated client for Modus API operations"""
    base_url: str = "http://localhost:3000/api"
    api_key: str
    session: requests.Session = requests.Session()
    async_session: aiohttp.ClientSession = None

    class Config:
        arbitrary_types_allowed = True

    def _get_headers(self):
        return {
            "accept": "application/json",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_predicates(self, project_id: str) -> Dict[str, Any]:
        """Fetch predicates for a document"""
        url = f"{self.base_url}/functions/{project_id}/predicates"
        response = self.session.get(url, headers=self._get_headers())
        return self._handle_response(response)

    def validate_assignment(self, project_id: str, assignments: Dict[str, bool]) -> Dict[str, Any]:
        """Validate truth assignments"""

        url = f"{self.base_url}/functions/{project_id}/validate"
        response = self.session.post(
            url,
            json={"assignments": assignments},
            headers=self._get_headers()
        )
        return self._handle_response(response)

    async def aget_predicates(self, project_id: str) -> Dict[str, Any]:
        """Async fetch predicates"""
        url = f"{self.base_url}/functions/{project_id}/predicates"
        async with self._get_async_session() as session:
            async with session.get(url, headers=self._get_headers()) as response:
                return await self._ahandle_response(response)

    async def avalidate_assignment(self, project_id: str, assignments: Dict[str, bool]) -> Dict[str, Any]:
        """Async validate assignments"""
        url = f"{self.base_url}/functions/{project_id}/validate"
        async with self._get_async_session() as session:
            async with session.post(
                url,
                json={"assignments": assignments},
                headers=self._get_headers()
            ) as response:
                return await self._ahandle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code != 200 and response.status_code != 422:
            error = response.json()
            raise ValueError(f"Modus API Error ({response.status_code}): {error}")
        return response.json()

    async def _ahandle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        if response.status != 200 and response.status_code != 422:
            error = await response.json()
            raise ValueError(f"Modus API Error ({response.status}): {error}")
        return await response.json()

    def _get_async_session(self):
        return self.async_session or aiohttp.ClientSession()
