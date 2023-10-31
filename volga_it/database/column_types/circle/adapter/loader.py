from psycopg import InterfaceError
from psycopg.adapt import Loader

from .type import PostgresCircle


class CircleLoader(Loader):
    def load(self, data: bytes):
        if isinstance(data, memoryview):
            data = bytes(data)

        v = data.decode()
        if v == "None":
            return None

        try:
            return PostgresCircle.from_string(v)
        except ValueError:
            raise InterfaceError("bad circle representation: %r" % v)
