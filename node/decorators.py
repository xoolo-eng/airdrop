def connection(connection):
    """
        Decorator for adding to the decorated function
        object to connect to the host.
    """
    def check_connection(function):
        def wrapper(**kwargs):
            if not kwargs.get("connection"):
                if connection.isConnected():
                    kwargs["connection"] = connection
                else:
                    raise ConnectionError("No connection to the blockchain node.")
            result = function(**kwargs)
            return result
        return wrapper
    return check_connection
