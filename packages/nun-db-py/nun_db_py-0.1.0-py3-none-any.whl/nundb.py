import asyncio
import websockets
from typing import Dict, List, Callable
from data_types.pending import PendingPromise
from handlers.response import ResponseHandler
import re

class NunDB:
    """
    NunDB Client for interacting with the NunDB WebSocket server. This class provides methods to
    authenticate, manage databases, manipulate keys, and set up watchers for key changes.
    """

    def __init__(self, url: str, name: str, pwd: str):
        """
        Initialize a NunDB client instance.

        :param url: The WebSocket server URL.
        :param name: Username for authentication.
        :param pwd: Password for authentication.
        """
        self.url = url
        self.name = name
        self.pwd = pwd
        self.websocket = None
        self.listener_task = None
        self.pending_promises = []
        self.should_show_logs = False
        self.watchers: Dict[str, List[Callable[[object], None]]] = {}

    async def connect(self, url: str, name: str, pwd: str):
        """
        Connect to the NunDB WebSocket server and authenticate.

        :param url: The WebSocket server URL.
        :param name: Username for authentication.
        :param pwd: Password for authentication.
        """
        self.websocket = await websockets.connect(url)
        print(f"Connected to: {url}")
        await self.send_command(f"auth {name} {pwd}")
        self.listener_task = asyncio.create_task(self.listener())

    async def send_command(self, command: str):
        """
        Send a command to the NunDB server asynchronously.

        :param command: The command to send to the server.
        :raises Exception: If the WebSocket connection is not established.
        """
        if self.websocket is None:
            raise Exception("Not connected to server. Use 'connect' method first.")

        await self.websocket.send(command)
        if self.should_show_logs:
            print(f"Command sent: {command}")

    def create_pending_promise(self, key: str, command: str) -> PendingPromise:
        """
        Create a PendingPromise instance for tracking asynchronous commands.

        :param key: The key associated with the promise.
        :param command: The command being executed.
        :return: A new PendingPromise instance.
        """
        return PendingPromise(key, command)

    def remove_pending_promises_by_key(self, key: str):
        """
        Remove a specific PendingPromise associated with a key.

        :param key: The key whose associated PendingPromise should be removed.
        """
        self.pending_promises = [
            promise for promise in self.pending_promises if promise.get_key() != key
        ]

    async def listener(self):
        """
        Continuously listen for responses from the WebSocket server.

        This method processes incoming messages and invokes appropriate handlers
        based on the message type.
        """
        while True:
            try:
                response = await self.websocket.recv()

                message_parts = re.split(r"[ \n]+", response)
                message_parts = [item for item in message_parts if ':' not in item and item != '']

                command = message_parts[0]

                # Handle different types of responses
                ResponseHandler.all_databases(command, message_parts, self.pending_promises)
                ResponseHandler.keys(command, message_parts, self.pending_promises)
                ResponseHandler.invalid_auth(response)
                ResponseHandler.no_database_selected(response)
                ResponseHandler.no_valid_database_name(response)
                ResponseHandler.getting_values(command, message_parts, self.pending_promises)
                ResponseHandler.watching_values(command, message_parts, self.pending_promises, self.execute_all_watchers)

                if self.should_show_logs:
                    print(f"Received Response: {response}")
            except websockets.ConnectionClosed:
                print("Connection closed by server.")
                break

    async def auth(self, name: str, pwd: str):
        """
        Authenticate with the NunDB server.

        :param name: Username for authentication.
        :param pwd: Password for authentication.
        """
        await self.send_command(f'auth {name} {pwd}')

    async def create_db(self, db_name: str, db_token: str):
        """
        Create a new database.

        :param db_name: The name of the new database.
        :param db_token: The token associated with the database.
        """
        await self.send_command(f'create-db {db_name} {db_token}')

    async def increment(self, key: str, value: int):
        """
        Increment a key's value by the specified amount.

        :param key: The key to increment.
        :param value: The amount to increment the key by.
        """
        await self.send_command(f'increment {key} {value}')

    async def remove(self, key: str):
        """
        Remove a key from the database.

        :param key: The key to remove.
        """
        await self.send_command(f'remove {key}')

    async def create_user(self, username: str, password: str):
        """
        Create a new user.

        :param username: The username of the new user.
        :param password: The password of the new user.
        """
        await self.send_command(f'create-user {username} {password}')

    async def get_value_safe(self, key: str):
        """
        Safely retrieve the value of a key.

        :param key: The key whose value should be retrieved.
        :return: The value of the key.
        """
        await self.send_command(f'get-safe {key}')

        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise(key, 'get-safe')

        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )

        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )

        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    def show_logs(self, active: bool):
        """
        Enable or disable logging of commands and responses.

        :param active: Set to True to enable logs, False to disable them.
        """
        self.should_show_logs = active

    async def get(self, key: str):
        """
        Retrieve the value of a key.

        :param key: The key to retrieve.
        :return: The value of the key.
        """
        return await self.get_value_safe(key)

    async def set(self, name: str, value: str):
        """
        Set a key to a specific value.

        :param name: The key to set.
        :param value: The value to assign to the key.
        """
        await self.set_value(name, value)

    async def set_value(self, name: str, value: str):
        """
        Alias for set method.

        :param name: The key to set.
        :param value: The value to assign to the key.
        """
        await self.set_value_safe(name, value, -1)

    async def set_value_safe(self, name: str, value: str, version: int):
        """
        Safely set a key to a specific value with version control.

        :param name: The key to set.
        :param value: The value to assign to the key.
        :param version: The version of the key to update.
        """
        await self.send_command(f'set-safe {name} {version} {value}')

    async def use_db(self, db_name: str, db_token: str):
        """
        Select a database for subsequent operations.

        :param db_name: The name of the database to use.
        :param db_token: The token associated with the database.
        """
        await self.send_command(f'use-db {db_name} {db_token}')

    async def add_watch(self, name: str, cb: Callable[[object], None]):
        """
        Add a watcher to monitor changes to a specific key.

        :param name: The key to monitor.
        :param cb: A callback function to execute when the key changes.
        """
        pending_promise = self.create_pending_promise(name, "watch-sent")
        self.pending_promises.append(pending_promise)
        await self.send_command(f"watch {name}")
        self.watchers.setdefault(name, []).append(cb)

    async def remove_all_watchers(self):
        """
        Remove all watchers and disable all notifications.
        """
        await self.send_command("unwatch-all")
        self.watchers.clear()

    async def remove_watcher(self, name: str):
        """
        Remove all watchers for a specific key.

        :param name: The key whose watchers should be removed.
        """
        if name in self.watchers and self.watchers[name]:
            await asyncio.sleep(0.1)
        await self.send_command(f"unwatch {name}")
        self.watchers.pop(name, None)

    def execute_all_watchers(self, key: str, data: object):
        """
        Execute all watchers associated with a specific key.

        :param key: The key that was changed.
        :param data: The data associated with the change.
        """
        if key in self.watchers:
            for watcher in self.watchers[key]:
                watcher(data)

    async def get_all_databases(self):
        """
        Retrieve a list of all databases.

        :return: A list of database names.
        """
        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise("", "dbs-list")
        await self.send_command("debug list-dbs")
        
        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )
        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )

        
        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    async def all_keys(self):
        """
        Retrieve all keys from the current database.

        :return: A list of keys.
        """
        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise("", "keys")
        await self.send_command("keys ")
        
        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )
        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )

        
        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    async def keys_starting_with(self, prefix: str):
        """
        Retrieve all keys that start with a given prefix.

        :param prefix: The prefix to filter keys.
        :return: A list of matching keys.
        """
        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise(prefix, "keys")
        await self.send_command(f"keys {prefix}*")
        
        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )
        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )
        
        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    async def keys_ending_with(self, suffix: str):
        """
        Retrieve all keys that end with a given suffix.

        :param suffix: The suffix to filter keys.
        :return: A list of matching keys.
        """
        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise(suffix, "keys")
        await self.send_command(f"keys *{suffix}")
        
        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )
        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )
        
        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    async def keys_contains(self, supposed_text: str):
        """
        Retrieve all keys that contain a given substring.

        :param supposed_text: The substring to filter keys.
        :return: A list of matching keys.
        """
        result_promise = asyncio.Future()
        pending_promise = self.create_pending_promise(supposed_text, "keys")
        await self.send_command(f"keys {supposed_text}")
        
        pending_promise.get_promise().add_done_callback(
            lambda future: result_promise.set_result(future.result())
        )
        
        pending_promise.get_promise().add_done_callback(
            lambda _: self.pending_promises.remove(pending_promise)
        )

        self.pending_promises.append(pending_promise)
        await asyncio.gather(pending_promise.get_promise())
        return await result_promise

    async def close(self):
        """
        Close the WebSocket server connection.

        This method also cancels the listener task if it's running.
        """
        if self.websocket:
            await self.websocket.close()
            if hasattr(self, 'listener_task'):
                self.listener_task.cancel()
                try:
                    await self.listener_task
                except asyncio.CancelledError:
                    pass

    @classmethod
    async def create(cls, url: str, name: str, pwd: str):
        """
        Create an instance of NunDB and automatically connect to the server.

        :param url: The WebSocket server URL.
        :param name: Username for authentication.
        :param pwd: Password for authentication.
        :return: An instance of NunDB.
        """
        instance = cls(url, name, pwd)
        await instance.connect(url, name, pwd)
        return instance
