"""Used for defining proxy class


"""


class Proxy:
    """

    Attributes:
        host:
        port:
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def to_string(self):
        return self.__str__()

    def __str__(self):
        return f'{self.host}:{self.port}'
