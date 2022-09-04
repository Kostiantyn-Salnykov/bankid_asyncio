import abc


class BankIDClientInterface(abc.ABC):
    @abc.abstractmethod
    def auth(self, **kwargs):
        ...

    @abc.abstractmethod
    def sign(self, **kwargs):
        ...

    @abc.abstractmethod
    def collect(self, **kwargs):
        ...

    @abc.abstractmethod
    def cancel(self, **kwargs):
        ...


class BankIDFactoryInterface(abc.ABC):
    @abc.abstractmethod
    def make_client(self) -> BankIDClientInterface:
        ...
