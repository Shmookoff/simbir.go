from psycopg import InterfaceError
from psycopg.adapt import Loader

from .type import PostgresCircle


class CircleLoader(Loader):
    def load(self, data: str | None):
        if data is None:
            return None

        try:
            return PostgresCircle.from_string(data)
        except ValueError:
            raise InterfaceError("bad circle representation: %r" % data)
