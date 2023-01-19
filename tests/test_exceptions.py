import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio import (
    AlreadyInProgressException,
    BankIDException,
    InternalErrorException,
    InvalidParametersException,
    MaintenanceErrorException,
    Messages,
    MethodNotAllowedException,
    NotFoundException,
    RequestTimeoutException,
    UnauthorizedException,
    UnhandledException,
    UnsupportedMediaTypeException,
    exception_handler,
)


class TestBankIDException:
    def test__repr__(self, faker: Faker):
        message, code, details = Messages.RFA5.value, faker.pyint(), faker.pystr()
        expected_result = f'{BankIDException.__name__}(message="{message}", code={code}, details="{details}")'

        result = BankIDException(message=message, code=code, details=details).__repr__()

        assert result == expected_result

    def test__str__(self, faker: Faker):
        message, code, details = Messages.RFA5.value, faker.pyint(), faker.pystr()
        expected_result = f'{BankIDException.__name__}(message="{message}", code={code}, details="{details}")'

        result = BankIDException(message=message, code=code, details=details).__str__()

        assert result == expected_result

    def test_dict(self, faker: Faker):
        message, code, details = Messages.RFA5.value, faker.pyint(), faker.pystr()
        expected_result = {"message": message, "code": code, "details": details}
        result = BankIDException(message=message, code=code, details=details).dict()

        assert result == expected_result


def test_exception_handler_success(mocker: MockerFixture, faker: Faker):
    expected_result = faker.pydict()
    response_mock = mocker.MagicMock(
        status_code=faker.pyint(min_value=200, max_value=399), json=mocker.MagicMock(return_value=expected_result)
    )

    result = exception_handler(response=response_mock)

    assert result == expected_result


@pytest.mark.parametrize(
    argnames=["status_code", "error_code", "exception", "message"],
    argvalues=[
        (400, "alreadyInProgress", AlreadyInProgressException, Messages.RFA4.value),
        (400, "invalidParameters", InvalidParametersException, ""),
        (401, "unauthorized", UnauthorizedException, ""),
        (403, "unauthorized", UnauthorizedException, ""),
        (404, "notFound", NotFoundException, ""),
        (405, "methodNotAllowed", MethodNotAllowedException, ""),
        (405, "", MethodNotAllowedException, ""),
        (408, "requestTimeout", RequestTimeoutException, Messages.RFA5.value),
        (415, "unsupportedMediaType", UnsupportedMediaTypeException, ""),
        (500, "internalError", InternalErrorException, Messages.RFA5.value),
        (503, "maintenance", MaintenanceErrorException, Messages.RFA5.value),
        # Unhandled error:
        *(
            (Faker().pyint(min_value=400, max_value=500), "test", UnhandledException, Messages.RFA22.value)
            for i in range(0, 4)
        ),
    ],
)
def test_exception_handler_error(
    status_code: int,
    error_code: str,
    exception: BankIDException,
    message: Messages,
    mocker: MockerFixture,
    faker: Faker,
):
    details = faker.pystr()
    response_mock = mocker.MagicMock(
        status_code=status_code,
        json=mocker.MagicMock(return_value={"status_code": status_code, "errorCode": error_code, "details": details}),
    )

    with pytest.raises(expected_exception=exception) as exception_context:
        exception_handler(response=response_mock)

    assert str(exception_context.value) == str(
        exception(message=message or error_code, code=status_code, details=details)
    )
