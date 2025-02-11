import logging
from enum import Enum
from typing import (
    Any,
    List,
    Optional,
)

from httpx import AsyncClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class HttpClientResponse(BaseModel):
    status: int
    error: Optional[Any] = None
    data: Optional[Any] = None


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class CoinSchema(BaseModel):
    id: str
    symbol: str
    name: str


class CoinListSchema(BaseModel):
    status: int
    coins: Optional[List[CoinSchema]]


class BaseHttpClient:
    def __init__(self):
        self._timeout = 10

    async def request(
        self,
        url: str,
        method: str = HTTPMethod.GET,
        service_name: Optional[str] = "HTTP Service",
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, Any]] = None,
        cookies: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> HttpClientResponse:

        kwargs.setdefault("headers", headers)
        kwargs.setdefault("params", params)
        kwargs.setdefault("cookies", cookies)

        async with AsyncClient(timeout=self._timeout) as client:
            request_msg = f"Request(method={method.upper()}, url={url})"
            try:
                response = await getattr(client, method)(url, **kwargs)
                response.raise_for_status()
                return HttpClientResponse(status=response.status_code, data=response.json())
            except Exception as exc:
                detail = f"Service: {service_name} - HTTP Client: {request_msg} failed. Reason: {str(exc)}"
                logger.error(detail)
                return HttpClientResponse(status=response.status_code, error=detail)


class CoingeckoApiSettings(BaseSettings):
    URL: str = "https://api.coingecko.com/api/v3/"
    TOKEN_NAME: str = "x_cg_demo_api_key"
    TOKEN: str = "CG-dUAPfzxd32y9NATpbH5Y8asa"


class CoingeckoApiService:
    service_name = "Coingecko API"

    def __init__(
        self,
        client: BaseHttpClient,
        settings: CoingeckoApiSettings,
    ) -> None:
        self._client = client
        self._settings = settings
        self._endpoint = "coins/list"

    async def get_coin_list(self) -> CoinListSchema:
        response = await self._client.request(
            url=f"{self._settings.URL}{self._endpoint}",
            headers={self._settings.TOKEN_NAME: self._settings.TOKEN},
            service_name=self.service_name,
        )

        return CoinListSchema(status=response.status, coins=response.data)
