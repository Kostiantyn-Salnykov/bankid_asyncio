import typing

import httpx

from bankid_asyncio.messages import Messages

__all__ = [
    "AlreadyInProgressException",
    "BankIDException",
    "exception_handler",
    "InternalErrorException",
    "InvalidParametersException",
    "MaintenanceErrorException",
    "MethodNotAllowedException",
    "NotFoundException",
    "RequestTimeoutException",
    "UnauthorizedException",
    "UnhandledException",
    "UnsupportedMediaTypeException",
]


class BankIDException(Exception):
    def __init__(self, *, message: typing.Union[Messages, str], code: int = 200, details: str = ""):
        self.message = message.value if isinstance(message, Messages) else message
        self.code = code
        self.details = details

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(message="{self.message}", code={self.code}, details="{self.details}")'

    def __str__(self) -> str:
        return self.__repr__()

    def dict(self) -> dict:
        return {"message": self.message, "code": self.code, "details": self.details}


class AlreadyInProgressException(BankIDException):
    ...


class InvalidParametersException(BankIDException):
    ...


class UnhandledException(BankIDException):
    ...


class UnauthorizedException(BankIDException):
    ...


class NotFoundException(BankIDException):
    ...


class MethodNotAllowedException(BankIDException):
    ...


class RequestTimeoutException(BankIDException):
    ...


class UnsupportedMediaTypeException(BankIDException):
    ...


class InternalErrorException(BankIDException):
    ...


class MaintenanceErrorException(BankIDException):
    ...


def exception_handler(response: httpx.Response) -> typing.Optional[typing.Dict[str, str]]:
    status_code: int = response.status_code
    response_json: typing.Dict[str, typing.Any] = response.json()
    if str(status_code).startswith(("2", "3")):  # Skip 2** and 3** status codes
        return response_json
    error_code = response_json.get("errorCode", None)
    details = response_json.get("details", "")
    errors_dict: typing.Dict[typing.Tuple[int, str], Exception] = {
        (400, "alreadyInProgress"): AlreadyInProgressException(
            message=Messages.RFA4, code=status_code, details=details
        ),
        (400, "invalidParameters"): InvalidParametersException(
            message=f"{error_code}", code=status_code, details=details
        ),
        (401, "unauthorized"): UnauthorizedException(message=f"{error_code}", code=status_code, details=details),
        (403, "unauthorized"): UnauthorizedException(message=f"{error_code}", code=status_code, details=details),
        (404, "notFound"): NotFoundException(message=f"{error_code}", code=status_code, details=details),
        (405, "methodNotAllowed"): MethodNotAllowedException(
            message=f"{error_code}", code=status_code, details=details
        ),
        (405, ""): MethodNotAllowedException(message=f"{error_code}", code=status_code, details=details),
        (408, "requestTimeout"): RequestTimeoutException(message=Messages.RFA5, code=status_code, details=details),
        (415, "unsupportedMediaType"): UnsupportedMediaTypeException(
            message=f"{error_code}", code=status_code, details=details
        ),
        (500, "internalError"): InternalErrorException(message=Messages.RFA5, code=status_code, details=details),
        (503, "maintenance"): MaintenanceErrorException(message=Messages.RFA5, code=status_code, details=details),
    }
    default_error = UnhandledException(message=Messages.RFA22, code=status_code, details=details)
    raise errors_dict.get((status_code, error_code), default_error)
