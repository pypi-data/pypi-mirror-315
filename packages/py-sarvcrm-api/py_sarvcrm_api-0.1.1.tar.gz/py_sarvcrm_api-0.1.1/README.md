# SarvClient API Interaction Module

## Overview

The **SarvClient** module provides a Python interface for interacting with the SarvCRM API. It simplifies authentication, CRUD operations, and module-specific functionalities for seamless integration with SarvCRM.

[SarvCRM API Documents](https://app.sarvcrm.com/webservice/)

## Features
- **Authentication**: Log in and manage sessions with the SarvCRM API.
- **CRUD Operations**: Perform Create, Read, Update, and Delete transactions via simple methods.
- **Context Manager Support**: Automatically handle login and logout within `with` statements.
- **Localization**: Supports specifying the desired language for API interactions.
- **Utility Methods**: Format dates, times, and other helper functionalities compliant with SarvCRM standards.

---

## Installation

1. Ensure you have Python 3.11+ installed.
2. Make Sure pip and git are installed
3. Install the package
   ```bash
   pip install py-sarvcrm-api
   ```

---

## Quick Start

### Example Usage

```python
from sarvcrm_api import SarvClient, SarvURL

# SarvURL = 'https://app.sarvcrm.com/API.php'

# Initialize the client
client = SarvClient(
    base_url=SarvURL, # you can specify your own url if you have local server
    utype="youre_instance_utype",
    username="your_username",
    password="your_password",
    language="en_US"
)

# Use as a context manager for clean execution
print(f'Connecting to {SarvURL}')
with client:
    # Create new item in Accounts
    uid = client.Accounts.create(type='Corporate', name='RadinSystem', numbers=['02145885000'])
    print(f'New Account Created: {uid}')
    
    # Read one item record
    record = clinet.Accounts.read_record(uid)
    print(f'Single Account record: {record}')

    # Read List of items
    records = client.Accounts.read_list(order_by='name')
    print('Accounts list:')
    for account in Accounts:
        print(f' - {account}')

    # Update an item
    updated_item = client.Accounts.update(uid, name='Radin-System')
    print(f'Updated item id: {updated_item}')

    # Search for data by phone number
    result = client.search_by_number(number="02145885000", module=client.Accounts) # module is optional
    print(f'Search by number result: {result}')

    # Delete Item
    deleted_item = client.Accounts.delete(uid)
    print(f'Deleted item: {deleted_item}')

```

---

## Class Details

### `SarvClient`

#### Constructor
```python
SarvClient(
    base_url: str,
    utype: str,
    username: str,
    password: str,
    login_type: Optional[str] = None, # eg. 'portal' for portal users
    language: str = "en_US", # Options: fa_IR, en_US
    is_password_md5: bool = False
)
```

**Parameters**:
- `base_url`: The base URL for the SarvCRM API.
- `utype`: Utype of your sarvcrm instance.
- `username`: Your SarvCRM username.
- `password`: Password for authentication.
- `login_type`: (Optional) Login type for advanced configurations.
- `language`: Language code (default: `en_US`).
- `is_password_md5`: Whether the password is already MD5-hashed.

---

### Methods

#### `iso_time_output`
Formats `datetime` or `timedelta` objects according to SarvCRM standards.

#### `login`
Authenticates the user and retrieves an access token.

#### `logout`
Clears the session token.

#### `search_by_number`
Searches a module or all modules for records matching a given phone number.

---

**Attributes**:
- `Accounts`, `AosContracts`, `AosInvoices`, `AosPdfTemplates`, etc.: Module instances for various SarvCRM functionalities.

**Description**:
Initializes all the modules as attributes of the `ModulesMixin` class for easy access.

---

### `SarvModule`

#### Constructor
```python
SarvModule(_client: SarvClient)
```

**Attributes**:
- `_module_name`: The name of the module.
- `_label_en`: The label of the module in English.
- `_label_pr`: The label of the module in Persian.
- `_client`: The `SarvClient` instance for API interactions.

#### Methods

- `create(**KWArgs) -> str`
    Creates a new record in the module.

- `read_list(query: Optional[str] = None, order_by: Optional[str] = None, select_fields: Optional[list[str]] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list`
    Retrieves a list of items from the module.

- `read_record(pk: str) -> dict`
    Fetches a single record by ID.

- `update(pk: str, **fields_data) -> str`
    Updates an existing record.

- `delete(pk: str) -> str | None`
    Deletes a record by ID.

- `get_module_fields() -> dict[str, dict]`
    Retrieves the fields of the module.

- `get_relationships(related_field: str, query: Optional[str] = None, order_by: Optional[str] = None, select_fields: Optional[list[str]] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list`
    Fetches related items.

- `save_relationships(pk: str, field_name: str, related_records: list) -> list`
    Saves relationships between records.

---

## Additional Features

- **Error Handling**: Raise `SarvException` for API errors.
- **Secure Defaults**: Passwords are hashed with MD5 unless explicitly provided as pre-hashed.

---

## License

This module is licensed for Radin System. For details, see the [LICENSE](LICENSE) file.
