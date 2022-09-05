# bankid-asyncio 🏦

--8<-- "docs/includes/badges.md"

## Dependencies ⛓

[![Pydantic](https://img.shields.io/badge/pydantic-%5E1.10.1-orange)](https://pydantic-docs.helpmanual.io/)
[![HTTPX](https://img.shields.io/badge/httpx-%5E0.23.0-orange)](https://www.python-httpx.org/)

## Description 📖
**bankid-asyncio** - is a BankID client for Python with asyncio support.

Asynchronous realization turned out to be implemented due to the fact that the library is written based on HTTPX, which 
allows not only synchronous requests (**Client**), but also asynchronous ones (**AsyncClient**).

## Install 💾

### pip
```{.terminal linenums="0"}
pip install bankid-asyncio
```

### Poetry
```{.terminal linenums="0"}
poetry add bankid-asyncio
```

## BankID

### Links 🖇
#### [BankID](https://www.bankid.com/en){.md-button target=_blank}
#### [BankID Relying Party Guidelines .pdf](https://www.bankid.com/assets/bankid/rp/BankID-Relying-Party-Guidelines-v3.7.pdf){.md-button target=_blank}

#### [BankID Best Practices](https://www.bankid.com/en/utvecklare/guider/praxis/praxis-anvaendarfall){.md-button target=_blank}
#### [BankID Formatting text](https://www.bankid.com/en/utvecklare/guider/formatera-text/formatera-text-introduktion){.md-button target=_blank}

### How it works❓
#### Success Auth/Sign flow
Starts on - Desktop or web

BankID used on - Mobile device
![HowTo Diagram](diagrams/out/howto.png)
