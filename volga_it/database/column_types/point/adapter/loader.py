from psycopg import InterfaceError
from psycopg.adapt import Loader

from .type import PostgresPoint


class PointLoader(Loader):
    def load(self, data: bytes):
        if isinstance(data, memoryview):
            data = bytes(data)

        v = data.decode()
        if v == "None":
            return None

        try:
            return PostgresPoint.from_string(v)
        except ValueError:
            raise InterfaceError("bad point representation: %r" % v)
