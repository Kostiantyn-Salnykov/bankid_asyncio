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

__all__ = ["BankIDSyncPydanticClient"]


class BankIDSyncPydanticClient(BankIDBaseClient):
    def __init__(self, *, host: str, certificate: str, key: str) -> None:
        certificate_file = temporary_pem_file(data=certificate)
        key_file = temporary_pem_file(data=key, name="key")
        self._http_client = httpx.Client(
            verify=False,  # no need to verify custom SSL certificates for BankID.
            cert=(certificate_file.name, key_file.name),  # Set Certificate & Key for request to BankID
            base_url=host,
            headers={"Content-Type": "application/json"},
        )

    @property
    def http_client(self) -> httpx.Client:
        return self._http_client

    def send(self, *, schema: SchemaType, endpoint: Endpoints) -> typing.Dict[str, str]:
        response = self.http_client.post(url=endpoint, json=schema.dict(exclude_unset=True, by_alias=True))
        return exception_handler(response=response)

    def auth(self, *, schema: AuthRequestSchema) -> AuthResponseSchema:
        raw_response = self.send(schema=schema, endpoint=Endpoints.AUTH)
        return AuthResponseSchema(**raw_response)

    def sign(self, *, schema: SignRequestSchema) -> SignResponseSchema:
        raw_response = self.send(schema=schema, endpoint=Endpoints.SIGN)
        return SignResponseSchema(**raw_response)

    def collect(self, *, schema: CollectRequestSchema) -> CollectResponseSchema:
        raw_response = self.send(schema=schema, endpoint=Endpoints.COLLECT)
        return CollectResponseSchema(**raw_response)

    def cancel(self, *, schema: CancelRequestSchema) -> None:
        self.send(schema=schema, endpoint=Endpoints.CANCEL)
        return None
