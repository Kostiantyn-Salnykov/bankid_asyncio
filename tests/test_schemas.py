import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio.schemas import (
    AuthRequestSchema,
    BaseAuthRequestSchema,
    CollectResponseSchema,
    CollectStatus,
    SignRequestSchema,
)


class TestBaseAuthRequestSchema:
    def test_validate_user_ip(self, faker: Faker):
        ip_value = faker.ipv4()

        result = BaseAuthRequestSchema.validate_user_ip(v=ip_value)

        assert result == ip_value

    def test_validate_user_ip_invalid(self, faker: Faker):
        ip_value = faker.pystr()

        with pytest.raises(ValueError) as exception_context:
            BaseAuthRequestSchema.validate_user_ip(v=ip_value)

        assert str(exception_context.value) == str(ValueError("Invalid user IPv4."))

    def test_validate_personal_number(self, personal_number):
        result = BaseAuthRequestSchema.validate_personal_number(v=personal_number)

        assert result == personal_number

    def test_validate_personal_number_invalid(self, faker: Faker):
        personal_number = faker.pystr()

        with pytest.raises(ValueError) as exception_context:
            BaseAuthRequestSchema.validate_personal_number(v=personal_number)

        assert str(exception_context.value) == str(
            ValueError("Invalid Personal Number, should be `YYYYMMDDNNNN` (12 digits).")
        )


class TestAuthRequestSchema:
    def test_validate_data_fields(self, faker: Faker, mocker: MockerFixture):
        value, expected_result = faker.pystr(), faker.pystr()
        validate_and_encode_base64_mock = mocker.patch(
            target="bankid_asyncio.schemas.validate_and_encode_base64", return_value=expected_result
        )

        result = AuthRequestSchema.validate_data_fields(v=value)

        validate_and_encode_base64_mock.assert_called_once_with(value=value, max_length=1500)
        assert result == expected_result


class TestSignRequestSchema:
    def test_validate_visible_data(self, faker: Faker, mocker: MockerFixture):
        value, expected_result = faker.pystr(), faker.pystr()
        validate_and_encode_base64_mock = mocker.patch(
            target="bankid_asyncio.schemas.validate_and_encode_base64", return_value=expected_result
        )

        result = SignRequestSchema.validate_visible_data(v=value)

        validate_and_encode_base64_mock.assert_called_once_with(value=value, max_length=40000)
        assert result == expected_result

    def test_validate_non_visible_data(self, faker: Faker, mocker: MockerFixture):
        value, expected_result = faker.pystr(), faker.pystr()
        validate_and_encode_base64_mock = mocker.patch(
            target="bankid_asyncio.schemas.validate_and_encode_base64", return_value=expected_result
        )

        result = SignRequestSchema.validate_non_visible_data(v=value)

        validate_and_encode_base64_mock.assert_called_once_with(value=value, max_length=200000)
        assert result == expected_result


class TestCollectResponseSchema:
    def test_validate_fields_invalid_complete(self, faker: Faker):
        status = CollectStatus.COMPLETE
        values = {"status": status}

        with pytest.raises(ValueError) as exception_context:
            CollectResponseSchema.validate_fields(values=values)

        assert str(exception_context.value) == str(
            ValueError(f"Invalid response for {status} has no `CompletionData`.")
        )

    def test_validate_fields_invalid_pending(self, faker: Faker):
        status = CollectStatus.PENDING
        values = {"status": status}

        with pytest.raises(ValueError) as exception_context:
            CollectResponseSchema.validate_fields(values=values)

        assert str(exception_context.value) == str(ValueError(f"Invalid response for {status} has no `HintCode`."))
