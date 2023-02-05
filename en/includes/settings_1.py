import functools

from pydantic import BaseSettings, Field

__all__ = ["BankIDSettings"]


class _BankIDSettings(BaseSettings):
    BANK_ID_CERTIFICATE: str
    BANK_ID_HOST: str = Field(default="https://appapi2.test.bankid.com/rp/v5.1")
    BANK_ID_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "UTF-8"


@functools.lru_cache()
def get_bank_id_settings() -> _BankIDSettings:
    return _BankIDSettings()


BankIDSettings: _BankIDSettings = get_bank_id_settings()
