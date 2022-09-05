import typing

import httpx

from bankid_asyncio.clients.bases import BankIDBaseClient, build_auth_kwargs, build_sign_kwargs
from bankid_asyncio.enums import Endpoints
from bankid_asyncio.exceptions import exception_handler
from bankid_asyncio.helpers import temporary_pem_file

__all__ = ["BankIDSyncClient"]


class BankIDSyncClient(BankIDBaseClient):
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

    def auth(
        self,
        *,
        user_ip: str,
        personal_number: typing.Optional[str] = None,
        requirement: typing.Optional[typing.Dict[str, str]] = None,
        visible_data: typing.Optional[str] = None,
        non_visible_data: typing.Optional[str] = None,
        visible_data_format: typing.Optional[str] = "simpleMarkdownV1",
    ) -> typing.Dict[str, str]:
        json_data = build_auth_kwargs(
            user_ip=user_ip,
            personal_number=personal_number,
            requirement=requirement,
            visible_data=visible_data,
            non_visible_data=non_visible_data,
            visible_data_format=visible_data_format,
        )
        raw_response = self.http_client.post(url=Endpoints.AUTH, json=json_data)
        return exception_handler(response=raw_response)

    def sign(
        self,
        *,
        user_ip: str,
        visible_data: str,
        personal_number: typing.Optional[str] = None,
        requirement: typing.Optional[typing.Dict[str, str]] = None,
        non_visible_data: typing.Optional[str] = None,
        visible_data_format: typing.Optional[str] = "simpleMarkdownV1",
    ) -> typing.Dict[str, str]:
        json_data = build_sign_kwargs(
            user_ip=user_ip,
            visible_data=visible_data,
            personal_number=personal_number,
            requirement=requirement,
            non_visible_data=non_visible_data,
            visible_data_format=visible_data_format,
        )
        raw_response = self.http_client.post(url=Endpoints.SIGN, json=json_data)
        return exception_handler(response=raw_response)

    def collect(self, *, order_ref) -> typing.Dict[str, str]:
        raw_response = self.http_client.post(url=Endpoints.COLLECT, json={"order_ref": order_ref})
        return exception_handler(response=raw_response)

    def cancel(self, *, order_ref: str):
        raw_response = self.http_client.post(url=Endpoints.CANCEL, json={"order_ref": order_ref})
        return exception_handler(response=raw_response)
