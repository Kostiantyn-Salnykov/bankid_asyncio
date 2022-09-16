# Usage 🔌

## Settings Management
### With Pydantic
Pydantic provides a convenient interface for managing settings and reading them from environment variables or `.env`.

Pydantic settings management:

[Documentation](https://pydantic-docs.helpmanual.io/usage/settings/){.md-button target=_blank}

Here is an example how you can manage your BankID environments:

!!! tip "settings.py"
    ```{.python linenums="0"}
    --8<-- "docs/includes/settings_1.py"
    ```

### With Dynaconf
Another good option to manage your settings and environments.

[https://www.dynaconf.com/](https://www.dynaconf.com/){.md-button target=_blank}


## BankID Factory 🏦🏭
To initialize BankID you should use `BankIDFactory` class and then use `make_client` method to retrieve necessary 
client.
```{.python linenums="0" hl_lines="5-9"}
--8<-- "docs/includes/factory_1.py"
```

## Clients 

### Key differences
#### With Pydantic
Clients with Pydantic require `schema` kwarg only attribute to all methods. It also returns BaseModel based results from 
all methods (all Pydantic features included).

It helps to easily transform results to complex structures written by schemas, that you can access with `.` dot 
notation, like class attributes, transform to dict with aliases and python snake case attribute names. 

#### Asynchronous
Clients with asyncio support, based on `httpx.AsyncClient`.

#### Synchronous
Clients, that based on `httpx.Client`.

### Async with Pydantic (preferable)

!!! help "Why this one preferable?"
    Because clients with Pydantic have extra validations (realization via `BaseModel` schema classes).
    It should prevent errors at develop & testing stages.

To use asynchronous BankID client with Pydantic use `:::py asynchronous=True` together with `:::py pydantic=True` inside
`make_client` method.
```{.python linenums="0" hl_lines="15"}
--8<-- "docs/includes/async_1.py"
```

!!! warning "TODO"
    Make demo (example purposes) repository with FastAPI based back-end using this client.

!!! warning
    async methods (coroutines) should be run from async code.


### Async without ~~Pydantic~~
To use asynchronous BankID client without ~~Pydantic~~ use `:::py asynchronous=True` together with 
`:::py pydantic=False` inside `make_client` method.
```{.python linenums="0" hl_lines="10"}
--8<-- "docs/includes/async_without_pydantic_1.py"
```

!!! warning
    async methods (coroutines) should be run from async code.


### Sync with Pydantic
To use synchronous BankID client with Pydantic use `:::py asynchronous=False` together with 
`:::py pydantic=True` inside `make_client` method.
```{.python linenums="0" hl_lines="15"}
--8<-- "docs/includes/sync_1.py"
```

??? example "Example output"
    ```{.bash linenums="0"}
    66d2323a-40a0-49e2-822d-f95f2fdc1c58 556080cd-aa51-4c37-82e8-f34d6dcebf4b 36d7f12b-52f5-44c4-9514-2a5d3d2b22d8 33b73952-f2dd-4c99-a727-c7ae77bdc834
    {'order_ref': '66d2323a-40a0-49e2-822d-f95f2fdc1c58', 'auto_start_token': '556080cd-aa51-4c37-82e8-f34d6dcebf4b', 'qr_start_token': '36d7f12b-52f5-44c4-9514-2a5d3d2b22d8', 'qr_start_secret': '33b73952-f2dd-4c99-a727-c7ae77bdc834'} {"order_ref": "66d2323a-40a0-49e2-822d-f95f2fdc1c58", "auto_start_token": "556080cd-aa51-4c37-82e8-f34d6dcebf4b", "qr_start_token": "36d7f12b-52f5-44c4-9514-2a5d3d2b22d8", "qr_start_secret": "33b73952-f2dd-4c99-a727-c7ae77bdc834"}
    {'orderRef': '66d2323a-40a0-49e2-822d-f95f2fdc1c58', 'autoStartToken': '556080cd-aa51-4c37-82e8-f34d6dcebf4b', 'qrStartToken': '36d7f12b-52f5-44c4-9514-2a5d3d2b22d8', 'qrStartSecret': '33b73952-f2dd-4c99-a727-c7ae77bdc834'} {"orderRef": "66d2323a-40a0-49e2-822d-f95f2fdc1c58", "autoStartToken": "556080cd-aa51-4c37-82e8-f34d6dcebf4b", "qrStartToken": "36d7f12b-52f5-44c4-9514-2a5d3d2b22d8", "qrStartSecret": "33b73952-f2dd-4c99-a727-c7ae77bdc834"}
    ```

### Sync without ~~Pydantic~~
To use synchronous BankID client without ~~Pydantic~~ use `:::py asynchronous=False` together with 
`:::py pydantic=False` inside `make_client` method.
```{.python linenums="0" hl_lines="10"}
--8<-- "docs/includes/sync_without_pydantic_1.py"
```

??? example "Example output"
    ```{.bash linenums="0"}
    {'orderRef': 'f7508caf-5e3c-40ed-b8a0-b47e3b82819f', 'autoStartToken': '45dd8454-9b43-4b3d-bbe8-ced64056d415', 'qrStartToken': '19f814b1-a198-4328-be1f-83a02f46890a', 'qrStartSecret': '663fee80-0a25-40a3-8d1b-a5c4046c01f1'}
    ```