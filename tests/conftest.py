import random
import typing

import pytest
from faker import Faker


@pytest.fixture(scope="function", autouse=True)
def faker_seed() -> int:
    """Generate random seed for Faker instance.

    Returns:
        Random generated integer from 0 up to 100000.
    """
    return random.randint(0, 100000)


@pytest.fixture()
def certificate() -> str:
    return """
    -----BEGIN CERTIFICATE-----
MIIEyjCCArKgAwIBAgIILFi5Qu2eUu4wDQYJKoZIhvcNAQELBQAwcTELMAkGA1UE
BhMCU0UxHTAbBgNVBAoMFFRlc3RiYW5rIEEgQUIgKHB1YmwpMRUwEwYDVQQFEwwx
MTExMTExMTExMTExLDAqBgNVBAMMI1Rlc3RiYW5rIEEgUlAgQ0EgdjEgZm9yIEJh
bmtJRCBUZXN0MB4XDTIwMDYxNzIyMDAwMFoXDTIyMDkwNTIxNTk1OVowcjELMAkG
A1UEBhMCU0UxHTAbBgNVBAoMFFRlc3RiYW5rIEEgQUIgKHB1YmwpMRMwEQYDVQQF
Ewo1NTY2MzA0OTI4MRcwFQYDVQQpDA5UZXN0IGF2IEJhbmtJRDEWMBQGA1UEAwwN
RlAgVGVzdGNlcnQgMzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMCb
Fluh4O4TEl4vydPGIUc4kAFDSVk1RM5TDYn8UDlWVxHVbalbXaJbtNQFYFm7lmpk
FXiif50iupanvIq+k4DIGm01MnGasWl4EW9uoExCoZC4EemZry+Hk7hm2vbwGudf
uIR8P43AD1MV7kp/skJaTH16qEeWTKQSoVlC+XNP/7Tl6Z8JE1GOR3+oAXWs+f/o
5SxXq4kIlBPkSK3tiTbEAP0/dNnSqSprv5MFHnTTWZyl8TK02TGrazyVUp/em6e6
V/lTtJylBmHNJMpzl7PGixgXApRSMj4ltHwjqAizBMatDoXE6qXG0fEj+vhqSo/v
wajY9t6FHNovhNdI+CcCAwEAAaNlMGMwEQYDVR0gBAowCDAGBgQqAwQFMA4GA1Ud
DwEB/wQEAwIHgDAfBgNVHSMEGDAWgBTiuVUIvGKgRjldgAxQSpIBy0zvizAdBgNV
HQ4EFgQU8xDQD1mLJ7MpUSxGB4lUDC5pdgswDQYJKoZIhvcNAQELBQADggIBAGWn
PRoXUxPITv9Uo+4llmIHhHg5XR5ejenJOFyCvTAtteQozdFJ2rby+Q4WZNAdtP8Q
tWcDaDigylDZSwi9TBGTRPSLH2cDFEWCQZVHs8svsF5VyBfkdtaRomiSAsk9KKLf
6Vo6ik1hlh4+NTBMX3VW0LjUZrPXmQ14El/XiJmHOvs54kAYf9ZTcO332Gqo8RF+
M3CRDVxPSrU34u6fvvxQuAvXvPumWvHaSAkOhpsn+Idr+KQ0Rip6fmgTG7UMicUi
PxTE66xpaMsHDmuPaeC+cTK/iXAW60+X/Vv/ANn7UOz6tvrjo6Sd1DIpEEjqW/yE
L4F05lbXhixKS2IRY+mAejoC66N2tz+0bv1grK4147jsYw4i9Y/rGyggkSrRd+1k
QM7uBxW3Cu5fSKOUZ/0UTcBGf82Ze8SlbFFvpagELy9cJHwMKarzTkuX92hJ9KG0
h26JBdOHzberG2tQiYzMPYVcch7WCAFWR++w6qInFs0WK7F7SBP0fyZew3hZZDoO
snqLWMgG+YagjAsMAcr99RvwqX7TJtISejdxz9lxxN2jKM0b1f2v8K88tzRekrGG
CPUQlnPu7sj7nPLVs5/sUEbaVRz8G8lKjYGsMuecRLpuVRQ/vPAd5whfiIzQFK76
boWGbSHS6OXfIfDrowTNlzAP+/H9f7DyBZTdwrVX
-----END CERTIFICATE-----
    """.replace(
        "\n", ""
    ).strip()


@pytest.fixture()
def key() -> str:
    return """
    -----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDAmxZboeDuExJe
L8nTxiFHOJABQ0lZNUTOUw2J/FA5VlcR1W2pW12iW7TUBWBZu5ZqZBV4on+dIrqW
p7yKvpOAyBptNTJxmrFpeBFvbqBMQqGQuBHpma8vh5O4Ztr28BrnX7iEfD+NwA9T
Fe5Kf7JCWkx9eqhHlkykEqFZQvlzT/+05emfCRNRjkd/qAF1rPn/6OUsV6uJCJQT
5Eit7Yk2xAD9P3TZ0qkqa7+TBR5001mcpfEytNkxq2s8lVKf3punulf5U7ScpQZh
zSTKc5ezxosYFwKUUjI+JbR8I6gIswTGrQ6FxOqlxtHxI/r4akqP78Go2PbehRza
L4TXSPgnAgMBAAECggEAdwrj5LrGxR7wiVpMCiI5S0XAa6dk3Eg6QLPAeHqEMwwU
QKeDYdtgogrAVxMDnDJ/Iz68rpTw/vQKEzeVJsPncv86pijtBp4v7RoS3KapWLkO
Ft5N4+3jAyNuv9iCmYGJf1wANZJ9zWTZk+bIIy+Nw8j/4cY/4A8bS4VgSEVG3GeQ
/uUODFXSoSIi0mHfz5JTg+Tk739fSIjKbE5jvtFMIjp7Buj/clowKn2JN+yDCYPQ
7hkJ5TDm9+fwuyZ7/sBW/0QrYOEiAkNYIGFOGffxJJKR6TtP4eV5qrCtVPnqxNyB
goEgZYbCh+3Ecslf6ZhSgLNreIy6OkTEarxJ6crwEQKBgQDZpu877IddIGqNRcxD
UzrmUueQSwaD76MNkCl9CwO+O9YlAm6cXCmbeq+2lzfGI47XAPlPfLAwCDHU4qEH
Eujunf47WmJEbh5BW8dPG/TOaMsPF+tgIEBIFKBg4+LFP9KYa49UZv4ak5SRm/lX
bZIDh7Lat5aRS28AqaiOY7xK2wKBgQDiinSk0K3u7WV7RmfU7ZvvG0maOKVBykND
xJS140UjC/oMjzxY9NIn4pZoR985g2sMC2NEwRX9RtuBk6lLTXqdDQBQT/ByWNZC
waF7XCuE1+8YEbuChFEKyQYqvn6YsjRzy2giNRQ+5ShggskqpXNlbNdJiRDUfDOV
Ht1Q1xj7pQKBgQCMxQZH+JQYLEYd9v3EsYkPvKEeVxfwr0YDGLFsuXoDSMoZB7io
kocqkzAgZS9ijE7vSib1PQzrE/G+4ZEKdTWIV1E97BhQb/RLi2OeC9PKyEZFDdBj
TJimxghwghOCReQcRrzd9vr0D21wu7OJ00kz1UldYo4UjPhPMmvdJC59LwKBgQDH
Q54iMuQrW2l+K4m9Q1t70HbHTrgdzHmqLEnaS5ROpYRGc99TJ9WK+8Xs5/szraMF
LyccHPLom+EMcwPglsAZUIxMGGSZUAb3JTaTOZmV+hH3C/Hxdc2LPRNNmc3lJir5
B5wLKsEqKYuAiMnF105PkpMzvXquTKlaq5FkQC9beQKBgQC4zeRihfM5V49YRzuo
bOj+5I1FVRgPHTqGMlNkzrzVk561kBSY6JfvPx4w5rylFTrBRM7IwwYNcnll0DVc
6cavNLs7O42rDEro5vAEpWiI6oMSGGtUsgzHTUENDxD36b/ZAGPshV8+J9cAdbgJ
BRCv1g4xLPJrOU6D66R4VUSrGg==
-----END PRIVATE KEY-----
    """.replace(
        "\n", ""
    ).strip()


@pytest.fixture()
def host() -> str:
    return "https://appapi2.test.bankid.com/rp/v5.1"


@pytest.fixture()
def auth_sign_response(faker: Faker) -> typing.Dict[str, str]:
    return {
        "orderRef": faker.uuid4(),
        "autoStartToken": faker.uuid4(),
        "qrStartToken": faker.uuid4(),
        "qrStartSecret": faker.uuid4(),
    }


@pytest.fixture()
def personal_number(faker: Faker) -> str:
    birth_date = faker.date_time_between(start_date="-90y").strftime("%Y%m%d")
    number = faker.pyint(min_value=1000, max_value=9999)
    return f"{birth_date}{number}"