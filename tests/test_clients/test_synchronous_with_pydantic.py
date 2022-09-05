from unittest.mock import MagicMock

import httpx
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio import (
    AuthResponseSchema,
    BankIDSyncPydanticClient,
    CollectResponseSchema,
    Endpoints,
    SignResponseSchema,
)


class TestBankIDSyncPydanticClient:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, faker: Faker, mocker: MockerFixture):
        self.temporary_pem_file_mock = mocker.patch(
            target="bankid_asyncio.clients.synchronous_with_pydantic.temporary_pem_file"
        )
        self.httpx_client_mock = mocker.patch.object(target=httpx, attribute="Client")
        self.schema_mock = MagicMock()

    @pytest.fixture(scope="function")
    def client(self, host: str, certificate: str, key: str) -> BankIDSyncPydanticClient:
        yield BankIDSyncPydanticClient(host=host, certificate=certificate, key=key)

    def test_http_client(self, host: str, certificate: str, key: str, client):
        result = client.http_client

        self.httpx_client_mock.assert_called_once_with(
            verify=False,
            base_url=host,
            cert=(
                self.temporary_pem_file_mock(data=certificate).name,
                self.temporary_pem_file_mock(data=key, name="key").name,
            ),
            headers={"Content-Type": "application/json"},
        )
        assert result == self.httpx_client_mock()

    def test_send(self, faker: Faker, mocker: MockerFixture, client):
        exception_handler_mock = mocker.patch(
            target="bankid_asyncio.clients.synchronous_with_pydantic.exception_handler"
        )

        result = client.send(schema=self.schema_mock, endpoint=Endpoints.AUTH)

        client.http_client.post.assert_called_once_with(
            url=Endpoints.AUTH, json=self.schema_mock.dict(exclude_unset=True, by_alias=True)
        )
        exception_handler_mock.assert_called_once_with(response=client.http_client.post())
        assert result == exception_handler_mock()

    def test_auth(self, faker: Faker, mocker: MockerFixture, client, auth_sign_response):
        send_mock = mocker.patch.object(
            target=BankIDSyncPydanticClient, attribute="send", return_value=auth_sign_response
        )

        result = client.auth(schema=self.schema_mock)

        send_mock.assert_called_once_with(schema=self.schema_mock, endpoint=Endpoints.AUTH)
        assert result == AuthResponseSchema(**auth_sign_response)

    def test_sign(self, faker: Faker, mocker: MockerFixture, client, auth_sign_response):
        send_mock = mocker.patch.object(
            target=BankIDSyncPydanticClient, attribute="send", return_value=auth_sign_response
        )

        result = client.sign(schema=self.schema_mock)

        send_mock.assert_called_once_with(schema=self.schema_mock, endpoint=Endpoints.SIGN)
        assert result == SignResponseSchema(**auth_sign_response)

    def test_collect(self, faker: Faker, mocker: MockerFixture, client):
        response_data = {}
        send_mock = mocker.patch.object(target=BankIDSyncPydanticClient, attribute="send", return_value=response_data)

        result = client.collect(schema=self.schema_mock)

        send_mock.assert_called_once_with(schema=self.schema_mock, endpoint=Endpoints.COLLECT)
        assert result == CollectResponseSchema(**response_data)

    def test_cancel(self, faker: Faker, mocker: MockerFixture, client):
        send_mock = mocker.patch.object(target=BankIDSyncPydanticClient, attribute="send", return_value={})

        result = client.cancel(schema=self.schema_mock)

        send_mock.assert_called_once_with(schema=self.schema_mock, endpoint=Endpoints.CANCEL)
        assert result is None
