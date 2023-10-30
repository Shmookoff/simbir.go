from psycopg import InterfaceError
from psycopg.adapt import Loader

from .type import PostgresPoint


class PointLoader(Loader):
    def load(self, data: str | None):
        if data is None:
            return None

        try:
            return PostgresPoint.from_string(data)
        except ValueError:
            raise InterfaceError("bad point representation: %r" % data)
