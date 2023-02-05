from bankid_asyncio import (
    BankIDFactory,
    BankIDSyncPydanticClient,
    AuthRequestSchema,
    AuthResponseSchema,
)
from settings import BankIDSettings

bank_id_factory = BankIDFactory(
    host=BankIDSettings.BANK_ID_HOST,
    certificate=BankIDSettings.BANK_ID_CERTIFICATE,
    key=BankIDSettings.BANK_ID_KEY,
)
bank_id_client: BankIDSyncPydanticClient = bank_id_factory.make_client(
    asynchronous=False, pydantic=True
)

auth_response: AuthResponseSchema = bank_id_client.auth(
    schema=AuthRequestSchema(user_ip="127.0.0.1")
)
# Possible usage of responses
print(
    auth_response.order_ref, auth_response.auto_start_token,
    auth_response.qr_start_token, auth_response.qr_start_secret,
)
print(auth_response.dict(), auth_response.json())
print(auth_response.dict(by_alias=True), auth_response.json(by_alias=True))
