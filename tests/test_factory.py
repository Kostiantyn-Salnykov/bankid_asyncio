import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio import (
    BankIDAsyncClient,
    BankIDAsyncPydanticClient,
    BankIDClientInterface,
    BankIDFactory,
    BankIDSyncClient,
    BankIDSyncPydanticClient,
)


class TestBankIDFactory:
    @pytest.mark.parametrize(
        argnames=["host", "formatted_host"],
        argvalues=[
            ("https://test.bank_id_factory.com/", "https://test.bank_id_factory.com"),
            ("https://test.bank_id_factory.com//", "https://test.bank_id_factory.com/"),
        ],
    )
    def test__init__(self, host: str, formatted_host: str, faker: Faker):
        result = BankIDFactory(host=host, certificate=faker.pystr(), key=faker.pystr())

        assert result._host == formatted_host

    @pytest.mark.parametrize(
        argnames=["asynchronous", "pydantic", "expected_instance"],
        argvalues=[
            (True, True, BankIDAsyncPydanticClient),
            (True, False, BankIDAsyncClient),
            (False, True, BankIDSyncPydanticClient),
            (False, False, BankIDSyncClient),
        ],
    )
    def test_make_client(
        self,
        asynchronous: bool,
        pydantic: bool,
        expected_instance: BankIDClientInterface,
        faker: Faker,
        mocker: MockerFixture,
    ):
        host, certificate, key = faker.uri(), faker.pystr(), faker.pystr()
        factory = BankIDFactory(host=host, certificate=certificate, key=key)
        mocker.patch.object(target=expected_instance, attribute="__init__", return_value=None)

        result = factory.make_client(asynchronous=asynchronous, pydantic=pydantic)

        assert isinstance(result, expected_instance)
