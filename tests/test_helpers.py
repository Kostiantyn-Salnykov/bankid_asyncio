import base64
import pathlib

import pytest
from faker import Faker

from bankid_asyncio import temporary_pem_file, validate_and_encode_base64, validate_uuid


def test_validate_and_encode_base64(faker: Faker):
    value = faker.pystr()
    expected_result = base64.b64encode(value.encode(encoding="UTF-8")).decode(encoding="UTF-8")

    result = validate_and_encode_base64(value=value, max_length=1000)

    assert result == expected_result


def test_validate_and_encode_base64_error(faker: Faker):
    max_length = faker.pyint(min_value=1, max_value=10000)
    value = faker.pystr(min_chars=max_length, max_chars=max_length + 1)

    with pytest.raises(ValueError) as exception_context:
        validate_and_encode_base64(value=value, max_length=max_length)

    assert str(exception_context.value) == str(ValueError(f"Base64 encoded value should be less than: {max_length}."))


def test_validate_uuid(faker: Faker):
    value = faker.uuid4()

    result = validate_uuid(value=value)

    assert result == value


def test_validate_uuid_error(faker: Faker):
    value = faker.pystr()

    with pytest.raises(ValueError) as exception_context:
        validate_uuid(value=value)

    assert str(exception_context.value) == str(ValueError("Invalid UUID4 value."))


def test_temporary_pem_file(faker: Faker):
    data: str = faker.pystr()

    file = temporary_pem_file(data=data)

    assert file.read() == data
    assert file.name.endswith(".pem")
    assert pathlib.Path(file.name).is_file()
    file.close()  # This actually deletes temporary file
    assert pathlib.Path(file.name).is_file() is False  # Temporary file deleted


@pytest.mark.parametrize(argnames="suffix", argvalues=[".pem", ".cert", ".something"])
def test_temporary_pem_file_custom_suffix(suffix: str, faker: Faker):
    data: str = faker.pystr()

    file = temporary_pem_file(data=data, suffix=suffix)

    assert file.read() == data
    assert file.name.endswith(suffix)
    assert pathlib.Path(file.name).is_file()
    file.close()  # This actually deletes temporary file
    assert pathlib.Path(file.name).is_file() is False  # Temporary file deleted
