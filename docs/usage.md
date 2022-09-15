# Usage 🔌

## Settings Management

Pydantic provides a convenient interface for managing settings and reading them from environment variables or `.env`.

Pydantic settings management:

[Documentation](https://pydantic-docs.helpmanual.io/usage/settings/){.md-button target=_blank}

Here is an example how you can manage your BankID environments:

!!! tip "settings.py"
```{.python linenums="0"}
--8<-- "docs/includes/settings_1.py"
```

## BankID Factory
To initialize BankID you should use `BankIDFactory` class and then use `make_client` method to retrieve necessary 
client.
```{.python linenums="0" hl_lines="5-9"}
--8<-- "docs/includes/async_1.py"
```

## Clients
### Async with Pydantic

To use asynchronous BankID client with Pydantic use `:::py asynchronous=True` together with `:::py pydantic=True` inside
`make_client` method.
```{.python linenums="0" hl_lines="15"}
--8<-- "docs/includes/async_2.py"
```
