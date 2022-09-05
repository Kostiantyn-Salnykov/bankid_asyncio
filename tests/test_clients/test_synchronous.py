import httpx
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio import BankIDSyncClient, Endpoints


class TestBankIDSyncClient:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, faker: Faker, mocker: MockerFixture):
        self.temporary_pem_file_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.temporary_pem_file")
        self.httpx_client_mock = mocker.patch.object(target=httpx, attribute="Client")

    @pytest.fixture(scope="function")
    def client(self, host: str, certificate: str, key: str) -> BankIDSyncClient:
        yield BankIDSyncClient(host=host, certificate=certificate, key=key)

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

    def test_auth(self, faker: Faker, mocker: MockerFixture, client):
        build_auth_kwargs_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.build_auth_kwargs")
        exception_handler_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.exception_handler")
        user_ip = faker.ipv4()

        result = client.auth(user_ip=user_ip)

        build_auth_kwargs_mock.assert_called_once_with(
            user_ip=user_ip,
            personal_number=None,
            requirement=None,
            visible_data=None,
            non_visible_data=None,
            visible_data_format="simpleMarkdownV1",
        )
        client.http_client.post.assert_called_once_with(url=Endpoints.AUTH, json=build_auth_kwargs_mock())
        exception_handler_mock.assert_called_once_with(response=client.http_client.post())
        assert result == exception_handler_mock()

    def test_sign(self, faker: Faker, mocker: MockerFixture, client):
        build_sign_kwargs_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.build_sign_kwargs")
        exception_handler_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.exception_handler")
        user_ip, visible_data = faker.ipv4(), faker.pystr()

        result = client.sign(user_ip=user_ip, visible_data=visible_data)

        build_sign_kwargs_mock.assert_called_once_with(
            user_ip=user_ip,
            visible_data=visible_data,
            personal_number=None,
            requirement=None,
            non_visible_data=None,
            visible_data_format="simpleMarkdownV1",
        )
        client.http_client.post.assert_called_once_with(url=Endpoints.SIGN, json=build_sign_kwargs_mock())
        exception_handler_mock.assert_called_once_with(response=client.http_client.post())
        assert result == exception_handler_mock()

    def test_collect(self, faker: Faker, mocker: MockerFixture, client):
        exception_handler_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.exception_handler")
        order_ref = faker.uuid4()

        result = client.collect(order_ref=order_ref)

        client.http_client.post.assert_called_once_with(url=Endpoints.COLLECT, json={"order_ref": order_ref})
        exception_handler_mock.assert_called_once_with(response=client.http_client.post())
        assert result == exception_handler_mock()

    def test_cancel(self, faker: Faker, mocker: MockerFixture, client):
        exception_handler_mock = mocker.patch(target="bankid_asyncio.clients.synchronous.exception_handler")
        order_ref = faker.uuid4()

        result = client.cancel(order_ref=order_ref)

        client.http_client.post.assert_called_once_with(url=Endpoints.CANCEL, json={"order_ref": order_ref})
        exception_handler_mock.assert_called_once_with(response=client.http_client.post())
        assert result == exception_handler_mock()
