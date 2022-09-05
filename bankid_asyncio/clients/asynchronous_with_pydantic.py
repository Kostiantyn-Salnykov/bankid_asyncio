import typing

import httpx

from bankid_asyncio.clients.bases import BankIDBaseClient
from bankid_asyncio.enums import Endpoints
from bankid_asyncio.exceptions import exception_handler
from bankid_asyncio.helpers import temporary_pem_file
from bankid_asyncio.schemas import (
    AuthRequestSchema,
    AuthResponseSchema,
    BaseSchema,
    CancelRequestSchema,
    CollectRequestSchema,
    CollectResponseSchema,
    SignRequestSchema,
    SignResponseSchema,
)

SchemaType = typing.TypeVar(name="SchemaType", bound=BaseSchema)

__all__ = ["BankIDAsyncPydanticClient"]


class BankIDAsyncPydanticClient(BankIDBaseClient):
    def __init__(self, *, host: str, certificate: str, key: str) -> None:
        certificate_file = temporary_pem_file(data=certificate)
        key_file = temporary_pem_file(data=key, name="key")
        self._http_client = httpx.AsyncClient(
            verify=False,  # no need to verify custom SSL certificates for BankID.
            cert=(certificate_file.name, key_file.name),  # Set Certificate & Key for request to BankID
            base_url=host,
            headers={"Content-Type": "application/json"},
        )

    @property
    def http_client(self) -> httpx.AsyncClient:
        return self._http_client

    async def send(self, *, schema: typing.Type[SchemaType], endpoint: Endpoints):
        response = await self.http_client.post(url=endpoint, json=schema.dict(exclude_unset=True, by_alias=True))
        return exception_handler(response=response)

    async def auth(self, *, schema: AuthRequestSchema) -> AuthResponseSchema:
        raw_response = await self.send(schema=schema, endpoint=Endpoints.AUTH)
        return AuthResponseSchema(**raw_response)

    async def sign(self, *, schema: SignRequestSchema) -> SignResponseSchema:
        raw_response = await self.send(schema=schema, endpoint=Endpoints.SIGN)
        return SignResponseSchema(**raw_response)

    async def collect(self, *, schema: CollectRequestSchema) -> CollectResponseSchema:
        raw_response = await self.send(schema=schema, endpoint=Endpoints.COLLECT)
        return CollectResponseSchema(**raw_response)

    async def cancel(self, *, schema: CancelRequestSchema) -> None:
        await self.send(schema=schema, endpoint=Endpoints.CANCEL)
        return None
