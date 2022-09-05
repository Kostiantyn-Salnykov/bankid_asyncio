from bankid_asyncio.clients.asynchronous import BankIDAsyncClient
from bankid_asyncio.clients.asynchronous_with_pydantic import BankIDAsyncPydanticClient
from bankid_asyncio.clients.bases import BankIDBaseClient
from bankid_asyncio.clients.synchronous import BankIDSyncClient
from bankid_asyncio.clients.synchronous_with_pydantic import BankIDSyncPydanticClient
from bankid_asyncio.interfaces import BankIDFactoryInterface

__all__ = ["BankIDFactory"]


class BankIDFactory(BankIDFactoryInterface):
    def __init__(self, *, host: str, certificate: str, key: str) -> None:
        self._host = host[:-1] if host.endswith("/") else host
        self._certificate = certificate
        self._key = key

    def make_client(self, *, asynchronous: bool = False, pydantic: bool = False) -> BankIDBaseClient:
        if asynchronous:
            if pydantic:
                client_class = BankIDAsyncPydanticClient
            else:
                client_class = BankIDAsyncClient
        else:
            if pydantic:
                client_class = BankIDSyncPydanticClient
            else:
                client_class = BankIDSyncClient
        return client_class(host=self._host, certificate=self._certificate, key=self._key)
