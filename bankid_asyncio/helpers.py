import base64
import tempfile
import typing
import uuid

__all__ = ["validate_and_encode_base64", "validate_uuid", "temporary_pem_file"]


def validate_and_encode_base64(*, value: str, max_length: int) -> str:
    b64_str = base64.b64encode(value.encode(encoding="UTF-8")).decode(encoding="UTF-8")
    if len(b64_str) > max_length:
        raise ValueError(f"Base64 encoded value should be less than: {max_length}.")
    return b64_str


def validate_uuid(value: str) -> str:
    try:
        uuid.UUID(value)
    except Exception as error:
        raise ValueError("Invalid UUID4 value.") from error
    return value


def temporary_pem_file(*, data: str, name: str = "cert", suffix: str = ".pem") -> typing.IO:
    file = tempfile.NamedTemporaryFile(mode="w+", prefix=name, suffix=suffix)
    # file.write(data.encode(encoding="ASCII"))
    file.write(data)
    file.seek(0)
    return file
