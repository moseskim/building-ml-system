import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict

import httpx
from pydantic import BaseModel
from src.middleware.json import json_serial
from src.schema.base_schema import UserRequest, UserResponse
from src.service.ab_test_service import Endpoint

logger = getLogger(__name__)


class UserIDs(BaseModel):
    user_ids: Dict[str, Endpoint]
    default_endpoint: Endpoint


class AbstractUserTestService(ABC):
    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 2,
    ):
        self.timeout = timeout
        self.retries = retries
        self.transport = httpx.AsyncHTTPTransport(
            retries=self.retries,
        )
        self.post_header: Dict[str, str] = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @abstractmethod
    async def route(
        self,
        request: UserRequest,
    ) -> UserResponse:
        raise NotImplementedError


class UserTestService(AbstractUserTestService):
    def __init__(
        self,
        user_ids: UserIDs,
        timeout: float = 10,
        retries: int = 2,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
        )
        self.user_ids = user_ids
        logger.info(f"initialized user ab test: {self.user_ids}")

    async def route(
        self,
        request: UserRequest,
    ) -> UserResponse:
        endpoint = self.user_ids.user_ids.get(request.user_id, self.user_ids.default_endpoint)
        return self.__route(
            request=request,
            endpoint=endpoint,
        )

    async def __route(
        self,
        request: UserRequest,
        endpoint: Endpoint,
    ) -> UserResponse:
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = await client.post(
                url=endpoint.endpoint,
                headers=self.post_header,
                data=json.dumps(request.request, default=json_serial),
            )
            try:
                res.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(e)
            data = res.json()
            response = UserResponse(
                endpoint=endpoint.endpoint,
                response=data,
            )
            return response
