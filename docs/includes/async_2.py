from bankid_asyncio import (
    BankIDFactory,
    BankIDAsyncPydanticClient,
    AuthRequestSchema,
    AuthResponseSchema,
)
from settings import BankIDSettings

bank_id_factory = BankIDFactory(
    host=BankIDSettings.BANK_ID_HOST,
    certificate=BankIDSettings.BANK_ID_CERTIFICATE,
    key=BankIDSettings.BANK_ID_KEY,
)
bank_id_client: BankIDAsyncPydanticClient = bank_id_factory.make_client(
    asynchronous=True, pydantic=True
)

auth_response: AuthResponseSchema = await bank_id_client.auth(
    schema=AuthRequestSchema(user_ip="127.0.0.1")
)
