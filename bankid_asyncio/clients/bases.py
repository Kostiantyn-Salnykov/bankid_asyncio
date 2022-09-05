import base64
import hashlib
import hmac
import time
import typing
import urllib.parse

from bankid_asyncio.interfaces import BankIDClientInterface

__all__ = ["BankIDBaseClient", "build_auth_kwargs", "build_sign_kwargs"]


class BankIDBaseClient(BankIDClientInterface):
    @staticmethod
    def generate_qr_code(*, qr_start_secret: str, qr_start_token: str, order_time: typing.Union[int, float]) -> str:
        qr_time_str = str(int(time.time() - order_time))  # "0", "1", "2", ...
        qr_auth_code: str = hmac.new(
            key=qr_start_secret.encode(), msg=qr_time_str.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        qr_data = f"bankid.{qr_start_token}.{qr_time_str}.{qr_auth_code}"
        return qr_data

    @staticmethod
    def generate_links(
        *, autostart_token: str, rp_ref: typing.Optional[str] = None, redirect: typing.Optional[str] = None
    ) -> typing.Dict[str, str]:
        data = {"autostarttoken": autostart_token, "redirect": redirect}
        if rp_ref:
            data.update({"rpref": base64.b64encode(rp_ref.encode(encoding="UTF-8")).decode(encoding="UTF-8")})
        return {
            "https_link": "https://app.bankid.com?" + urllib.parse.urlencode(query=data),
            "desktop_link": "bankid:///?" + urllib.parse.urlencode(query=data),
        }


def build_auth_kwargs(
    *,
    user_ip: str,
    personal_number: typing.Optional[str] = None,
    requirement: typing.Optional[typing.Dict[str, str]] = None,
    visible_data: typing.Optional[str] = None,
    non_visible_data: typing.Optional[str] = None,
    visible_data_format: typing.Optional[str] = "simpleMarkdownV1",
) -> typing.Dict[str, typing.Any]:
    json_data = {"endUserIp": user_ip}
    json_data.update({"personalNumber": personal_number}) if personal_number else ...
    json_data.update({"requirement": requirement}) if requirement else ...
    json_data.update({"userVisibleData": visible_data}) if visible_data else ...
    json_data.update({"userNonVisibleData": non_visible_data}) if non_visible_data else ...
    if json_data.get("userVisibleData", None):
        json_data.update({"userVisibleDataFormat": visible_data_format})
    return json_data


def build_sign_kwargs(
    *,
    user_ip: str,
    visible_data: str,
    personal_number: typing.Optional[str] = None,
    requirement: typing.Optional[typing.Dict[str, str]] = None,
    non_visible_data: typing.Optional[str] = None,
    visible_data_format: typing.Optional[str] = "simpleMarkdownV1",
) -> typing.Dict[str, typing.Any]:
    json_data = {
        "endUserIp": user_ip,
        "userVisibleData": visible_data,
        "userVisibleDataFormat": visible_data_format,
    }
    json_data.update({"personalNumber": personal_number}) if personal_number else ...
    json_data.update({"requirement": requirement}) if requirement else ...
    json_data.update({"userNonVisibleData": non_visible_data}) if non_visible_data else ...
    return json_data
