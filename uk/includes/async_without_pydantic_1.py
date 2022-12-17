from bankid_asyncio import BankIDFactory, BankIDAsyncClient
from settings import BankIDSettings

bank_id_factory = BankIDFactory(
    host=BankIDSettings.BANK_ID_HOST,
    certificate=BankIDSettings.BANK_ID_CERTIFICATE,
    key=BankIDSettings.BANK_ID_KEY,
)
bank_id_client: BankIDAsyncClient = bank_id_factory.make_client(
    asynchronous=True, pydantic=False
)

# === Async code ===
# Then you'll be able to use BankID client coroutines inside async code.
auth_response = await bank_id_client.auth(user_ip="127.0.0.1")
