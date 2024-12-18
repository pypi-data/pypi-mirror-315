# NunDB Client (Python)

NunDB Client for interacting with the NunDB WebSocket server. This Python client allows you to authenticate, manage databases, manipulate keys, and set up watchers for key changes in the NunDB server.

## Features

- **Connect to WebSocket**: Connect and authenticate with the NunDB WebSocket server.
- **Database Management**: Create and manage databases.
- **Key Management**: Set, get, increment, and remove keys.
- **Watchers**: Watch keys for changes and execute callbacks when changes occur.
- **Asynchronous**: Fully asynchronous, based on `asyncio` and `websockets` for non-blocking operations.

## Installation

To install the NunDB Python client, you can use `pip`:

```bash
pip install nun-db-py
```

# Usage
## Basic Usage Example


```python
import asyncio
from nun_db_client import NunDB

async def main():
    # Connect to the NunDB server
    url = "ws://localhost:9000"
    username = "your_username"
    password = "your_password"
    
    nun_db, _ = await NunDB.create(url, username, password)

    # Create a new database
    db_name = "test_db"
    db_token = "your_db_token"
    await nun_db.create_db(db_name, db_token)

    # Set a key-value pair
    await nun_db.set("some_key", "some_value")

    # Get the value of a key
    value = await nun_db.get("some_key")
    print(value)

    # Increment a key's value
    await nun_db.increment("some_key", 10)

    # Add a watcher for a key
    await nun_db.add_watch("some_key", lambda data: print(f"Key changed: {data}"))

    # Remove the watcher
    await nun_db.remove_watcher("some_key")

    # Close the connection
    await nun_db.close()

# Run the example
asyncio.run(main())

```

## Available Methods

- `connect(url: str, name: str, pwd: str)`: Connect to the NunDB WebSocket server and authenticate.
- `create_db(db_name: str, db_token: str)`: Create a new database.
- `set(name: str, value: str)`: Set a key to a specific value.
- `get(name: str)`: Get the value of a key.
- `increment(key: str, value: int)`: Increment the value of a key.
- `remove(key: str)`: Remove a key from the database.
- `add_watch(name: str, cb: Callable)`: Add a watcher for a key.
- `remove_watcher(name: str)`: Remove the watcher for a key.
- `close()`: Close the WebSocket connection.

## Watchers

You can set up watchers to listen for changes to a key. The callback function will be executed whenever the key is modified.

Example:
```python
await nun_db.add_watch("some_key", lambda data: print(f"Key {data} changed"))
```

## Advanced Usage

- **get_all_databases()**: Retrieve all databases.
- **keys_starting_with(prefix: str)**: Retrieve all keys starting with a given prefix.
- **keys_ending_with(suffix: str)**: Retrieve all keys ending with a given suffix.
- **keys_contains(supposed_text: str)**: Retrieve all keys that contain a specific substring.

## Error Handling

The client raises exceptions if commands fail. You should handle errors accordingly by wrapping them in try-except blocks.

## Logging

To enable logging for commands and responses:

```python
nun_db.show_logs(True)
```

## Closing the Connection

To close the WebSocket connection gracefully, use:

```python
await nun_db.close()
```

Dependencies

    asyncio
    websockets
    re

License

MIT License. See LICENSE for more details.