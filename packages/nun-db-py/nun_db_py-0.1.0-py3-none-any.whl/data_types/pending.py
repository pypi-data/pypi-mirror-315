import asyncio

class PendingPromise:
    def __init__(self, key: str, command: str):
        self.key = key
        self.command = command
        self.promise = asyncio.Future()

    def get_key(self):
        return self.key
    
    def get_command(self):
        return self.command
    
    def get_promise(self):
        return self.promise