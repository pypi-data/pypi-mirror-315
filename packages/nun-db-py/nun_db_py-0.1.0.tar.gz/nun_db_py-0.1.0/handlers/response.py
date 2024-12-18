
class ResponseHandler:
    @staticmethod
    def no_database_selected(message):
        if "no-db-selected" in message:
            raise Exception("Please select a database with useDb()")

    @staticmethod
    def no_valid_database_name(message):
        if "Not a valid database name" in message:
            raise Exception("Database not found on useDb()")

    @staticmethod
    def invalid_auth(message):
        if "invalid auth" in message:
            raise Exception("Invalid auth!")

    @staticmethod
    def all_databases(command, message_parts, pending_promises):
        if command == "dbs-list":
            for promise in pending_promises:
                if promise.get_command() == "dbs-list":
                    promise.get_promise().set_result(message_parts[1:])

    @staticmethod
    def cluster_state(command, message_parts, pending_promises):
        if command == "cluster-state":
            payload = message_parts[1] if len(message_parts) > 1 else ""
            raw_clusters = payload.replace(" ", "").replace(",", "").split(",")
            clusters = [part for part in raw_clusters if part]

            for promise in pending_promises:
                if promise.get_command() == "cluster-state":
                    promise.get_promise().set_result(clusters)

    @staticmethod
    def keys(command, message_parts, pending_promises):
        if command == "keys":
            payload = message_parts[1] if len(message_parts) > 1 else ""
            raw_parts = payload.split(",")
            keys = [part for part in raw_parts if part]

            for promise in pending_promises:
                if promise.get_command() == "keys":
                    promise.get_promise().set_result(keys)

    @staticmethod
    def getting_values(command, message_parts, pending_promises):
        if command == "value-version":
            payload = message_parts[1] if len(message_parts) > 1 else ""
            parts = payload.split(" ", 1)
            version = int(parts[0]) if len(parts) > 0 else -1
            key = parts[1] if len(parts) > 1 else ""

            for promise in pending_promises:
                if promise.get_command() == "get-safe":
                    promise.get_promise().set_result(message_parts[2])

    @staticmethod
    def watching_values(command, message_parts, pending_promises, execute_all_watchers):
        if command == "changed":
            payloads = message_parts[1] if len(message_parts) > 1 else ""
            parts = payloads.split()
            key = parts[0]
            value = message_parts[-1]


            for promise in pending_promises:
                if promise.get_command() == "watch-sent" :
                    execute_all_watchers(key, value)