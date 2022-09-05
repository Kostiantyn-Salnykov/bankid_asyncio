import base64
import hashlib
import hmac
import time
import urllib.parse

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from bankid_asyncio import BankIDBaseClient, build_auth_kwargs, build_sign_kwargs


class TestBankIDBaseClient:
    def test_generate_qr_code(self, faker: Faker, mocker: MockerFixture):
        hmac_digest_result = faker.pystr()
        hmac_mock = mocker.MagicMock(hexdigest=mocker.MagicMock(return_value=hmac_digest_result))
        hmac_new_mock = mocker.patch.object(target=hmac, attribute="new", return_value=hmac_mock)
        seconds_delta = faker.pyint(min_value=0, max_value=300)
        current_time = time.time()
        qr_start_secret, qr_start_token, order_time = faker.pystr(), faker.pystr(), current_time
        mocker.patch.object(target=time, attribute="time", return_value=current_time + seconds_delta)

        result = BankIDBaseClient.generate_qr_code(
            qr_start_secret=qr_start_secret, qr_start_token=qr_start_token, order_time=order_time
        )

        hmac_new_mock.assert_called_once_with(
            key=qr_start_secret.encode(), msg=f"{seconds_delta}".encode(), digestmod=hashlib.sha256
        )
        assert result == f"bankid.{qr_start_token}.{seconds_delta}.{hmac_digest_result}"

    def test_generate_links(self, faker: Faker):
        autostart_token = faker.uuid4()
        expected_query = {"autostarttoken": autostart_token, "redirect": None}

        result = BankIDBaseClient.generate_links(autostart_token=autostart_token)

        assert result == {
            "https_link": "https://app.bankid.com?" + urllib.parse.urlencode(query=expected_query),
            "desktop_link": "bankid:///?" + urllib.parse.urlencode(query=expected_query),
        }

    def test_generate_links_with_redirect(self, faker: Faker):
        autostart_token, redirect = faker.uuid4(), faker.uri()
        expected_query = {"autostarttoken": autostart_token, "redirect": redirect}

        result = BankIDBaseClient.generate_links(autostart_token=autostart_token, redirect=redirect)

        assert result == {
            "https_link": "https://app.bankid.com?" + urllib.parse.urlencode(query=expected_query),
            "desktop_link": "bankid:///?" + urllib.parse.urlencode(query=expected_query),
        }

    def test_generate_links_with_rp_ref(self, faker: Faker):
        autostart_token, rp_ref = faker.uuid4(), faker.uri()
        expected_query = {
            "autostarttoken": autostart_token,
            "redirect": None,
            "rpref": base64.b64encode(rp_ref.encode(encoding="UTF-8")).decode(encoding="UTF-8"),
        }

        result = BankIDBaseClient.generate_links(autostart_token=autostart_token, rp_ref=rp_ref)

        assert result == {
            "https_link": "https://app.bankid.com?" + urllib.parse.urlencode(query=expected_query),
            "desktop_link": "bankid:///?" + urllib.parse.urlencode(query=expected_query),
        }


def test_build_auth_kwargs(faker: Faker):
    user_ip = faker.ipv4()

    result = build_auth_kwargs(user_ip=user_ip)

    assert result == {"endUserIp": user_ip}


@pytest.mark.parametrize(
    argnames=["key", "expected_key"],
    argvalues=[
        ("personal_number", "personalNumber"),
        ("requirement", "requirement"),
        ("non_visible_data", "userNonVisibleData"),
    ],
)
def test_build_auth_kwargs_parametrized(key: str, expected_key: str, faker: Faker):
    data_kwargs = {"user_ip": faker.ipv4(), key: faker.pystr()}

    result = build_auth_kwargs(**data_kwargs)

    assert result == {"endUserIp": data_kwargs["user_ip"], expected_key: data_kwargs[key]}


def test_build_auth_kwargs_visible_data(faker: Faker):
    data_kwargs = {"user_ip": faker.ipv4(), "visible_data": faker.pystr()}
    expected_result = {
        "endUserIp": data_kwargs["user_ip"],
        "userVisibleData": data_kwargs["visible_data"],
        "userVisibleDataFormat": "simpleMarkdownV1",
    }

    result = build_auth_kwargs(**data_kwargs)

    assert result == expected_result


def test_build_auth_kwargs_format_only(faker: Faker):
    data_kwargs = {"user_ip": faker.ipv4(), "visible_data_format": faker.pystr()}
    # visible_data_format will be ignored (without visible_data)
    expected_result = {"endUserIp": data_kwargs["user_ip"]}

    result = build_auth_kwargs(**data_kwargs)

    assert result == expected_result


def test_build_sign_kwargs(faker: Faker):
    user_ip, visible_data = faker.ipv4(), faker.pystr()

    result = build_sign_kwargs(user_ip=user_ip, visible_data=visible_data)

    assert result == {
        "endUserIp": user_ip,
        "userVisibleData": visible_data,
        "userVisibleDataFormat": "simpleMarkdownV1",
    }


def test_build_sign_kwargs_custom_format(faker: Faker):
    user_ip, visible_data, data_format = faker.ipv4(), faker.pystr(), faker.pystr()

    result = build_sign_kwargs(user_ip=user_ip, visible_data=visible_data, visible_data_format=data_format)

    assert result == {
        "endUserIp": user_ip,
        "userVisibleData": visible_data,
        "userVisibleDataFormat": data_format,
    }


@pytest.mark.parametrize(
    argnames=["key", "expected_key"],
    argvalues=[
        ("personal_number", "personalNumber"),
        ("requirement", "requirement"),
        ("non_visible_data", "userNonVisibleData"),
    ],
)
def test_build_sign_kwargs_parametrized(key: str, expected_key: str, faker: Faker):
    data_kwargs = {"user_ip": faker.ipv4(), key: faker.pystr(), "visible_data": faker.pystr()}

    result = build_sign_kwargs(**data_kwargs)

    assert result == {
        "endUserIp": data_kwargs["user_ip"],
        expected_key: data_kwargs[key],
        "userVisibleData": data_kwargs["visible_data"],
        "userVisibleDataFormat": "simpleMarkdownV1",
    }
