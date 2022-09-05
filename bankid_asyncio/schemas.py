import ipaddress
import typing

from pydantic import BaseModel, Field, root_validator, validator

from bankid_asyncio.enums import CollectStatus
from bankid_asyncio.helpers import validate_and_encode_base64, validate_uuid

__all__ = [
    "AuthRequestSchema",
    "AuthResponseSchema",
    "BaseAuthRequestSchema",
    "BaseSchema",
    "CancelRequestSchema",
    "CertSchema",
    "CollectRequestSchema",
    "CollectResponseSchema",
    "CompletionDataSchema",
    "DeviceSchema",
    "RequirementSchema",
    "SignRequestSchema",
    "SignResponseSchema",
    "UserSchema",
]


class BaseSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class RequirementSchema(BaseSchema):
    card_reader: typing.Optional[str] = Field(default="class1", alias="cardReader")
    certificate_policies: typing.Optional[typing.List[str]] = Field(default=[], alias="certificatePolicies")
    issuer_cn: typing.Optional[str] = Field(default=None, alias="issuerCn")
    allow_fingerprint: typing.Optional[bool] = Field(default=False, alias="allowFingerprint")
    token_start_required: typing.Optional[bool] = Field(default=False, alias="tokenStartRequired")


class BaseAuthRequestSchema(BaseSchema):
    user_ip: str = Field(alias="endUserIp")
    personal_number: typing.Optional[str] = Field(default=None, alias="personalNumber")
    requirement: typing.Optional[RequirementSchema] = Field(default=None)

    @validator("user_ip")
    def validate_user_ip(cls, v: str) -> str:
        try:
            ipaddress.IPv4Address(v)
        except Exception:
            raise ValueError("Invalid user IPv4.")
        else:
            return v

    @validator("personal_number")
    def validate_personal_number(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 12:
            raise ValueError("Invalid Personal Number, should be `YYYYMMDDNNNN` (12 digits).")
        return v


class AuthRequestSchema(BaseAuthRequestSchema):
    visible_data: typing.Optional[str] = Field(default=None, alias="userVisibleData")
    non_visible_data: typing.Optional[str] = Field(default=None, alias="userNonVisibleData")
    visible_data_format: typing.Optional[str] = Field(default="simpleMarkdownV1", alias="userVisibleDataFormat")

    @validator("visible_data", "non_visible_data")
    def validate_data_fields(cls, v: str) -> str:
        max_length = 1500
        return validate_and_encode_base64(value=v, max_length=max_length)


class SignRequestSchema(BaseAuthRequestSchema):
    visible_data: str = Field(default=..., alias="userVisibleData")
    non_visible_data: typing.Optional[str] = Field(default=None, alias="userNonVisibleData")
    visible_data_format: typing.Optional[str] = Field(default="simpleMarkdownV1", alias="userVisibleDataFormat")

    @validator("visible_data")
    def validate_visible_data(cls, v: str) -> str:
        max_length = 40000
        return validate_and_encode_base64(value=v, max_length=max_length)

    @validator("non_visible_data")
    def validate_non_visible_data(cls, v: str) -> str:
        max_length = 200000
        return validate_and_encode_base64(value=v, max_length=max_length)


class AuthResponseSchema(BaseSchema):
    order_ref: str = Field(default=..., alias="orderRef")
    auto_start_token: str = Field(default=..., alias="autoStartToken")
    qr_start_token: str = Field(default=..., alias="qrStartToken")
    qr_start_secret: str = Field(default=..., alias="qrStartSecret")

    _validate_uuids = validator("order_ref", "auto_start_token", "qr_start_token", "qr_start_secret", allow_reuse=True)(
        validate_uuid
    )


class SignResponseSchema(AuthResponseSchema):
    ...


class CollectRequestSchema(BaseSchema):
    order_ref: str = Field(default=..., alias="orderRef")

    _validate_order_ref = validator("order_ref", allow_reuse=True)(validate_uuid)


class UserSchema(BaseSchema):
    personal_number: str = Field(alias="personalNumber")
    name: str
    given_name: str = Field(alias="givenName")
    surname: str


class DeviceSchema(BaseSchema):
    ip_address: str = Field(alias="ipAddress")


class CertSchema(BaseSchema):
    not_before: int = Field(alias="notBefore")
    not_after: int = Field(alias="notAfter")


class CompletionDataSchema(BaseSchema):
    user: UserSchema
    device: DeviceSchema
    cert: CertSchema
    signature: str
    ocsp_response: str = Field(alias="ocspResponse")


class CollectResponseSchema(BaseSchema):
    order_ref: typing.Optional[str] = Field(default=None, alias="orderRef")
    status: typing.Optional[CollectStatus] = Field(default=None)
    hint_code: typing.Optional[str] = Field(default=None, alias="hintCode")
    completion_data: typing.Optional[CompletionDataSchema] = Field(default=None, alias="completionData")

    @root_validator()
    def validate_fields(cls, values: dict) -> dict:
        status = values.get("status", None)
        if status == CollectStatus.COMPLETE and not values.get("completion_data", None):
            raise ValueError(f"Invalid response for {status} has no `CompletionData`.")
        elif status in (CollectStatus.PENDING, CollectStatus.FAILED) and not values.get("hint_code", None):
            raise ValueError(f"Invalid response for {status} has no `HintCode`.")
        return values


class CancelRequestSchema(BaseSchema):
    order_ref: str = Field(default=..., alias="orderRef")

    _validate_order_ref = validator("order_ref", allow_reuse=True)(validate_uuid)
