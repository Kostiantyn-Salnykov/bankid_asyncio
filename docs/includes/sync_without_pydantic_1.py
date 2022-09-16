from bankid_asyncio import BankIDFactory, BankIDSyncClient
from settings import BankIDSettings

bank_id_factory = BankIDFactory(
    host=BankIDSettings.BANK_ID_HOST,
    certificate=BankIDSettings.BANK_ID_CERTIFICATE,
    key=BankIDSettings.BANK_ID_KEY,
)
bank_id_client: BankIDSyncClient = bank_id_factory.make_client(
    asynchronous=False, pydantic=False
)

auth_response = bank_id_client.auth(user_ip="127.0.0.1")

# Results from clients is simple python's dict
print(auth_response)
